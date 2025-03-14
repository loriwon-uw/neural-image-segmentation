import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from matplotlib.pyplot import figure
from scipy import ndimage
import math
import copy
from fil_finder import FilFinder2D, Filament2D
import astropy.units as u
from .utils import *
from scipy.ndimage.morphology import binary_dilation


class SegmentationAnalysis:
    def __init__(self):
        self.axon_color = np.array([255, 129, 31])  # Axon color pixel mask
        self.cell_color = np.array([255, 0, 255])  # Cell color pixel mask
        self.img = []  # The original segmentation image in rgb color
        self.img_path = ""  # The file path for the loaded image
        # Labeled Info
        self.labeled_axon = []  # Labeled Axons with different numbers
        self.labeled_cell = []  # Labeled Cell Clusters with different numbers
        self.nr_cell = 0  # Total number of cell clusters
        self.nr_filtered_cell = 0  # Total number of cell clusters after filtering
        self.nr_filtered_cell_w_axon = 0  # Total number of filtered cell cluster with axon

        # Returned Results
        self.axons_to_cells = {}    # Cells that are connected to each axon
        self.fil = None     # Returned object from the fil-finder library
        self.info_list = []
        self.axon_adjacent = []
        self.segmented_axons = []
        self.show_orientation = []
        self.cell_boundary_mask = []
        self.cell_axons_map = []
        self.cell_pixels = []   # Pixels for each cell
        self.cell_area_map = {}     # Index map for the area of each cell
        self.segmented_axons_dist = []

    def readImg(self, path):
        # Save the file path for the image
        self.img_path = path
        # Open and save the original image which is in BGR mode
        img_ori = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        # Convert and save the BGR image into RGB image
        self.img = cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB)

    def separate_axon_and_cell(self):
        # Apply the axon and cell filter based on the pixel color
        axon_filter = cv2.inRange(self.img, self.axon_color, self.axon_color)
        cell_filter = cv2.inRange(self.img, self.cell_color, self.cell_color)
        # Save the axon mask and the number of axon clusters
        self.labeled_axon, nr_axon = ndimage.label(axon_filter)
        # Save the cell mask and the number of cell clusters
        self.labeled_cell, self.nr_cell = ndimage.label(cell_filter)

    def filter_cells(self, cell_filter_size):
        # Initialize the array to save the cell pixels for each index
        self.cell_pixels = [[] for j in range(self.nr_cell)]
        # Convert the filter size from the real area to number of pixels
        filter_size = cell_filter_size * 2.22 * 2.22
        # Initialize the number of filtered cells to the total number of cells found
        self.nr_filtered_cell = self.nr_cell
        # Iterate over the cell mask and calculate the area for each cell
        for i in range(len(self.labeled_cell)):
            for j in range(len(self.labeled_cell[0])):
                if self.labeled_cell[i][j] != 0:
                    self.cell_pixels[self.labeled_cell[i][j] - 1].append([i, j])
        for i in range(1, self.nr_cell + 1):
            area = np.isclose(i, self.labeled_cell).sum()
            # Check if the cell area meet the filtered size
            if area < filter_size:
                self.nr_filtered_cell -= 1
                self.labeled_cell[self.labeled_cell == i] = 0
                self.cell_pixels[self.labeled_cell[i][j] - 1].clear()
            else:
                # Map the index to the actual area of that cell
                self.cell_area_map[i] = area / 2.22 / 2.22

        k = np.ones((3, 3), dtype=int)  # for 4-connected
        # Obtain the mask for cell boundary
        self.cell_boundary_mask = binary_dilation(self.labeled_cell == 0, k) & (self.labeled_cell != 0)

    def get_touching_dict(self):
        # Make a copy of the labeled axon mask
        self.axon_adjacent = copy.deepcopy(self.labeled_axon)
        labeled_axon_np = np.array(self.labeled_axon)
        labeled_cell_np = np.array(self.labeled_cell)
        height = len(labeled_axon_np)
        width = len(labeled_axon_np[0])
        # Filter the pixels on the edges
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                # Filter the unlabeled axon pixels
                if self.axon_adjacent[i][j] == 0:
                    continue
                if labeled_cell_np[i - 1][j] != 0 or labeled_cell_np[i + 1][j] != 0 or \
                        labeled_cell_np[i][j - 1] != 0 or labeled_cell_np[i][j - 1] != 0:
                    if self.axon_adjacent[i][j] not in self.axons_to_cells.keys():
                        self.axons_to_cells[self.axon_adjacent[i][j]] = {}
                    if labeled_cell_np[i - 1][j] != 0:
                        touching_cell = labeled_cell_np[i - 1][j]
                    elif labeled_cell_np[i + 1][j] != 0:
                        touching_cell = labeled_cell_np[i + 1][j]
                    elif labeled_cell_np[i][j - 1] != 0:
                        touching_cell = labeled_cell_np[i][j - 1]
                    else:
                        touching_cell = labeled_cell_np[i][j + 1]
                    # The first index is the axon index, the second is the connected cell index
                    self.axons_to_cells[self.axon_adjacent[i][j]][touching_cell] = [i, j]

    def filter_axon(self):
        # Obtain the mask for axon pixels
        axon_filter = cv2.inRange(self.img, self.axon_color, self.axon_color)
        # Run the fil-finder library to get the line skeleton
        self.fil = FilFinder2D(axon_filter, distance=250 * u.pc, mask=axon_filter)
        self.fil.preprocess_image(flatten_percent=85)
        self.fil.create_mask(border_masking=True, verbose=False, use_existing_mask=True)
        self.fil.medskel(verbose=False)
        self.fil.analyze_skeletons(branch_thresh=20 * u.pix, skel_thresh=30 * u.pix, prune_criteria='length', max_prune_iter=10)
        # self.fil.analyze_skeletons(skel_thresh=10 * u.pix, prune_criteria='length')

    def analyze_axons(self):
        length_filament = len(self.fil.filaments)
        for i in range(length_filament):
            x = self.fil.filaments[i].pixel_coords[0][0]
            y = self.fil.filaments[i].pixel_coords[1][0]
            if not (self.axon_adjacent[x][y] in self.axons_to_cells.keys()):
                self.info_list.append({"touch_points": [], "end_points": [], "intersect_points": [], "dists": []})
                continue
            touching_points = self.axons_to_cells[self.axon_adjacent[x][y]]
            # The closest point to a cell on the axon skeleton
            touch_points = []
            # The end points of skeleton
            end_points = self.fil.filaments[i].end_pts
            # The intersection points between branches
            intersect_points = []
            # touching key represents the connected cell index
            for touching_key in touching_points.keys():
                touching_coord = touching_points[touching_key]
                # Get the pixel that is closest to the touching cell on the skeleton
                touch_point = getTouchingPoint(self.fil.filaments[i], touching_coord)
                touch_point.append(touching_key)
                touch_points.append(touch_point)
            for ele in self.fil.filaments[i].intersec_pts:
                for e in ele:
                    intersect_points.append(e)
            self.info_list.append(
                {"touch_points": touch_points, "end_points": end_points, "intersect_points": intersect_points})
        # self.displayInfoList()

    def displayInfoList(self):
        # Print each item inside the info list
        for info in self.info_list:
            print(info)

    def getLineSegments(self, i):
        # Separate one axon cluster into individual axon segments for analysis
        line_segments = []
        # The line segments that contain a touch point, subset of line segments
        touch_segments = set()
        # print(len(self.fil.filaments[i].branch_pts()))
        # print(self.info_list[i]["intersect_points"])
        for br_pts in self.fil.filaments[i].branch_pts():
            start_found = False
            for k in range(len(br_pts)):
                # Add the absolute coordinate to the relative coordinate
                br_pts[k] = list(br_pts[k])
                br_pts[k][0] += self.fil.filament_extents[i][0][0] - 1
                br_pts[k][1] += self.fil.filament_extents[i][0][1] - 1
                if not start_found:
                    for end_pt in self.info_list[i]["end_points"]:
                        if br_pts[k][0] == end_pt[0] and br_pts[k][1] == end_pt[1]:
                            if k > 0:
                                tem = br_pts[0].copy()
                                br_pts[0] = br_pts[k].copy()
                                br_pts[k] = tem
                            start_found = True
            index = 0
            while not start_found and index < len(br_pts):
                # Fix for intersection points not in the branch pixel array
                for inter in self.info_list[i]["intersect_points"]:
                    if close(br_pts[index], inter):
                        if index != 0:
                            tem = br_pts[0].copy()
                            br_pts[0] = br_pts[index].copy()
                            br_pts[index] = tem
                            np.insert(br_pts, 0, np.array(list(inter)))
                        start_found = True
                        break
                index += 1

            line = []
            # order the pixels inside the branch
            br_pts = order_pts(br_pts)
            # print(br_pts)
            for pt in br_pts:
                line.append(pt)
                if_touch1 = get_touch(pt, self.info_list[i]["touch_points"])
                if_touch2 = get_touch(line[0], self.info_list[i]["touch_points"])
                if (if_touch1 != -1 or if_touch2 != -1) and len(line) > 1:
                    touch_segments.add(len(line_segments))
                    line_segments.append(line.copy())
                    line = [pt]
            if len(line) > 1:
                if_touch1 = get_touch(line[0], self.info_list[i]["touch_points"])
                if_touch2 = get_touch(line[-1], self.info_list[i]["touch_points"])
                if if_touch2 != -1:
                    line.reverse()  # Make sure for touch segments the first element is the touch point
                if if_touch1 != -1 or if_touch2 != -1:
                    touch_segments.add(len(line_segments))
                line_segments.append(line.copy())

        # print(line_segments)
        # print(len(line_segments), touch_segments, self.info_list[i]["touch_points"])
        return line_segments, touch_segments

    def getSegmentedAxons(self):
        # Iterate over all the axon clusters to get all the touching point between axon and cell
        all_touch_points = []
        for i in range(len(self.info_list)):
            for ele in self.info_list[i]["touch_points"]:
                all_touch_points.append(ele)
        for i in range(len(self.info_list)):
            line_segments, touch_segments = self.getLineSegments(i)
            length = len(line_segments)
            # print(length, len(touch_segments))
            line_used = [False for j in range(length)]  # If the line segment is already used for another axon
            count = 0   # Count the number of used line segments
            for k in touch_segments:
                if line_used[k]:
                    continue
                line_used[k] = True
                count = count + 1
                prev_end = line_segments[k][-1]
                if arr_in(prev_end, all_touch_points):
                    line_segments[k].reverse()
                self.segmented_axons.append(line_segments[k])
                # self.segmented_axons_dist.append(cal_dist_ptp(line_segments[k]))
                self.segmented_axons_dist.append(cal_dist(line_segments[k]))
                prev_start = line_segments[k][0]
                prev_end = line_segments[k][-1]
                found = 0
                while count < length and found != -1:
                    found = -1
                    orientation_prox = -1    # Maximum proximity is 2560
                    for j in range(length):
                        if line_used[j]:
                            continue
                        length_j = cal_dist(line_segments[j])
                        pt_start_j = line_segments[j][0]
                        pt_end_j = line_segments[j][-1]
                        # if pt_end_j[0] == prev_end[0] and pt_end_j[1] == prev_end[1]:
                        if close(pt_end_j, prev_end):
                            line_segments[j].reverse()
                            pt_start_j = line_segments[j][0]
                            pt_end_j = line_segments[j][-1]
                        # Check if these two line segments are adjacent
                        # if pt_start_j[0] != prev_end[0] or pt_start_j[1] != prev_end[1] or arr_in(prev_end, all_touch_points):
                        if not close(pt_start_j, prev_end) or arr_in(prev_end, all_touch_points):
                            continue
                        # Assign new branches based on the orientation affinity
                        # TODO: Use more involved algorithm for assigning branches
                        ori1 = getOrientation(pt_start_j, pt_end_j)
                        ori2 = getOrientation(prev_start, prev_end)
                        ori_prox = abs(ori1 - ori2)
                        dist = cal_dist(line_segments[j])
                        # dist = cal_dist_ptp(line_segments[j])
                        if ori_prox > 180:
                            ori_prox = 360 - ori_prox
                        ori_prox = (1 + math.cos(math.radians(ori_prox))) * dist
                        if ori_prox > orientation_prox:
                            orientation_prox = ori_prox
                            found = j
                    if found != -1:
                        self.segmented_axons[-1] = self.segmented_axons[-1] + line_segments[found]
                        # self.segmented_axons_dist[-1] += cal_dist_ptp(line_segments[found])
                        self.segmented_axons_dist[-1] += cal_dist(line_segments[found])
                        line_used[found] = True
                        count += 1
                        prev_start = line_segments[found][0]
                        prev_end = line_segments[found][-1]
                    # if arr_in(prev_end, all_touch_points):
                    #     break
        # Setup for post analysis
        index_to_remove = []
        self.cell_axons_map = [[] for j in range(self.nr_cell)]

        # Remove the axons that don't reach 20 µm
        for i in range(len(self.segmented_axons)):
            # dist = pixel_to_length(cal_dist(self.segmented_axons[i]))
            # if self.segmented_axons_dist[i] > 150:
                # print(self.segmented_axons[i])
            if pixel_to_length(self.segmented_axons_dist[i]) <= 20:
                index_to_remove.append(i)
                continue
        index_to_remove.reverse()
        for i in index_to_remove:
            del self.segmented_axons[i]
            del self.segmented_axons_dist[i]
        # Generate a show orientation array indicating axons that are connected between two cells
        for i in range(len(self.segmented_axons)):
            touch_index1 = get_touch(self.segmented_axons[i][0], all_touch_points)
            if touch_index1 != -1:
                self.cell_axons_map[touch_index1 - 1].append(i)
            touch_index2 = get_touch(self.segmented_axons[i][-1], all_touch_points)
            if touch_index2 != -1:
                self.cell_axons_map[touch_index2 - 1].append(i)
            if touch_index1 != -1 and touch_index2 != -1:
                self.show_orientation.append(False)
            else:
                self.show_orientation.append(True)
        self.nr_filtered_cell_w_axon = 0
        for i in self.cell_axons_map:
            if i:
                self.nr_filtered_cell_w_axon += 1

    def run(self, path, img, cell_filter_size):
        # Load the loaded image from the application
        self.img = img
        # Get the image path
        self.img_path = path
        # Separate the axon and cell segmentation pixels
        self.separate_axon_and_cell()
        # Filter the cell clusters by size
        self.filter_cells(cell_filter_size)
        # Get the touching point of the cells and axons
        self.get_touching_dict()
        # Apply the FilFinder library
        self.filter_axon()
        # Get the information for analyzing axon segments
        self.analyze_axons()
        # Run a graph algorithm to separate axon clusters into individual axons
        self.getSegmentedAxons()
        return self.segmented_axons

    # return the cell pixel closest to (x, y)
    def clickOnPixel(self, x, y):
        r1, c1 = np.nonzero(self.labeled_cell)
        min_idx1 = ((r1 - x) ** 2 + (c1 - y) ** 2).argmin()
        return self.labeled_cell[r1[min_idx1]][c1[min_idx1]]
