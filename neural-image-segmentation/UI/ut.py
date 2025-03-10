# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from .viewer import ImageViewer


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.showMaximized()
        MainWindow.setMinimumSize(1500, 820)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 160, 170))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.preButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.preButton.setObjectName("preButton")
        self.verticalLayout.addWidget(self.preButton)

        # Add model selection drop-down menu
        # self.verticalLayout.addLayout(self.horizonlLayout)
        # self.modelSelectLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        # self.modelSelectLabel.setText('Model:')

        self.modelSelection = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.modelSelection.addItems(['Small Model', 'Large Model'])
        self.modelSelection.setObjectName("modelSelection")
        self.verticalLayout.addWidget(self.modelSelection)

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.analyzeButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.analyzeButton.setObjectName("analyzeButton")
        self.verticalLayout.addWidget(self.analyzeButton)

        self.horizonLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizonLayoutWidget.setGeometry(QtCore.QRect(190, 40, 860, 440))
        self.horizonLayoutWidget.setObjectName("horizonLayoutWidget")
        self.horizonLayout = QtWidgets.QHBoxLayout(self.horizonLayoutWidget)
        self.horizonLayout.setContentsMargins(0, 0, 0, 0)
        self.horizonLayout.setObjectName("horizonLayout")
        self.graphicsView1 = ImageViewer(self.horizonLayoutWidget)
        self.graphicsView1.setGeometry(QtCore.QRect(190, 40, 430, 440))
        self.graphicsView1.setObjectName("graphicsView1")
        self.horizonLayout.addWidget(self.graphicsView1)
        self.graphicsView2 = ImageViewer(self.horizonLayoutWidget)
        self.graphicsView2.setGeometry(QtCore.QRect(620, 40, 430, 440))
        self.graphicsView2.setObjectName("graphicsView2")
        self.horizonLayout.addWidget(self.graphicsView2)

        self.giflabel = QtWidgets.QLabel(self.horizonLayoutWidget)
        self.giflabel.setGeometry(QtCore.QRect(620, 40, 430, 440))
        self.giflabel.setMinimumSize(QtCore.QSize(430, 440))
        self.giflabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.giflabel.setStyleSheet("background-color:rgb(160, 160, 160)")
        self.giflabel.setObjectName("giflabel")
        self.horizonLayout.addWidget(self.giflabel)
        self.giflabel.hide()

        self.horizonLayoutWidget2 = QtWidgets.QWidget(self.centralWidget)
        self.horizonLayoutWidget2.setGeometry(QtCore.QRect(900, 490, 140, 40))
        self.horizonLayoutWidget2.setObjectName("verticalLayoutWidget2")
        self.horizonLayout2 = QtWidgets.QHBoxLayout(self.horizonLayoutWidget2)
        self.horizonLayout2.setContentsMargins(0, 0, 0, 0)
        self.horizonLayout2.setObjectName("verticalLayout2")
        # self.exportButton = QtWidgets.QPushButton(self.horizonLayoutWidget2)
        # self.exportButton.setObjectName("exportButton")
        # self.horizonLayout2.addWidget(self.exportButton)
        # self.saveButton = QtWidgets.QPushButton(self.horizonLayoutWidget2)
        # self.saveButton.setObjectName("saveButton")
        # self.horizonLayout2.addWidget(self.saveButton)
        self.clearButton = QtWidgets.QPushButton(self.horizonLayoutWidget2)
        self.clearButton.setObjectName("clearButton")
        self.horizonLayout2.addWidget(self.clearButton)
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralWidget)
        # self.graphicsView.setEnabled(True)
        # self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        # self.progressBar.setGeometry(QtCore.QRect(370, 390, 118, 23))
        # self.progressBar.setProperty("value", 24)
        # self.progressBar.setObjectName("progressBar")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(190, 10, 800, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName("textBrowser")
        self.toolButton = QtWidgets.QToolButton(self.centralWidget)
        self.toolButton.setGeometry(QtCore.QRect(1000, 10, 40, 25))
        self.toolButton.setObjectName("toolButton")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.infoboxLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.infoboxLayoutWidget.setGeometry(QtCore.QRect(1070, 10, 400, 450))
        self.infoboxLayoutWidget.setObjectName("verticalLayoutWidget3")
        self.cellAreaInfoboxLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.cellAreaInfoboxLayoutWidget.setGeometry(QtCore.QRect(1070, 470, 400, 350))
        self.cellAreaInfoboxLayoutWidget.setObjectName("verticalLayoutWidget4")
        self.infoboxLayout = QtWidgets.QVBoxLayout(self.infoboxLayoutWidget)
        self.infoboxLayout.setContentsMargins(0, 0, 0, 0)
        self.infoboxLayout.setObjectName("verticalLayout3")
        self.cellAreaInfoboxLayout = QtWidgets.QVBoxLayout(self.cellAreaInfoboxLayoutWidget)
        self.cellAreaInfoboxLayout.setContentsMargins(0, 0, 0, 0)
        self.cellAreaInfoboxLayout.setObjectName("verticalLayout4")
        self.info = QtWidgets.QLabel(self.infoboxLayoutWidget)
        self.info.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        self.info.setObjectName("label")
        # self.info.setFont(QtGui.QFont('Segoe UI', 15))
        self.info.setFont(QtGui.QFont('Times New Roman', 14))
        self.infoboxLayout.addWidget(self.info)

        self.cellInfoboxLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.cellInfoboxLayoutWidget.setGeometry(QtCore.QRect(190, 550, 860, 500))
        self.cellInfoboxLayoutWidget.setObjectName("horizontalLayoutWidget2")
        self.cellInfoboxLayout = QtWidgets.QVBoxLayout(self.cellInfoboxLayoutWidget)
        self.cellInfoboxLayout.setContentsMargins(0, 0, 0, 0)
        self.cellInfoboxLayout.setObjectName("horizontalLayout2")
        self.cellInfo = QtWidgets.QLabel(self.cellInfoboxLayoutWidget)
        self.cellInfo.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        self.cellInfo.setObjectName("label")
        self.cellInfo.setFont(QtGui.QFont('Times New Roman', 14))
        self.cellInfoboxLayout.addWidget(self.cellInfo)

        self.userInputLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.userInputLayoutWidget.setGeometry(QtCore.QRect(20, 200, 160, 240))
        self.userInputLayoutWidget.setObjectName("userinputLayoutWidget")
        self.userInputLayout = QtWidgets.QVBoxLayout(self.userInputLayoutWidget)
        self.userInputLayout.setContentsMargins(0, 0, 0, 0)
        self.userInputLayout.setObjectName("userInputLayout")
        # Set cell filter size
        self.cellFilterLabel = QtWidgets.QLabel(self.userInputLayoutWidget)
        self.cellFilterLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cellFilterLabel.setObjectName("cellFilterLabel")
        self.userInputLayout.addWidget(self.cellFilterLabel)
        self.cellFilterTextbox = QtWidgets.QLineEdit()
        self.cellFilterTextbox.setObjectName("cellFilter")
        self.cellFilterTextbox.setPlaceholderText("200")
        self.userInputLayout.addWidget(self.cellFilterTextbox)
        self.setFilterButton = QtWidgets.QPushButton(self.userInputLayoutWidget)
        self.setFilterButton.setObjectName("setFilterButton")
        self.userInputLayout.addWidget(self.setFilterButton)
        # Find cell of certain index
        self.cellIndexLabel = QtWidgets.QLabel(self.userInputLayoutWidget)
        self.cellIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cellIndexLabel.setObjectName("cellIndexLabel")
        self.userInputLayout.addWidget(self.cellIndexLabel)
        self.cellIndexTextbox = QtWidgets.QLineEdit()
        self.cellIndexTextbox.setObjectName("cellIndex")
        self.userInputLayout.addWidget(self.cellIndexTextbox)
        self.getCellIndexButton = QtWidgets.QPushButton(self.userInputLayoutWidget)
        self.getCellIndexButton.setObjectName("getCellIndexButton")
        self.userInputLayout.addWidget(self.getCellIndexButton)
        # Find axon of certain index
        self.axonIndexLabel = QtWidgets.QLabel(self.userInputLayoutWidget)
        self.axonIndexLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.axonIndexLabel.setObjectName("axonIndexLabel")
        self.userInputLayout.addWidget(self.axonIndexLabel)
        self.axonIndexTextbox = QtWidgets.QLineEdit()
        self.axonIndexTextbox.setObjectName("axonIndex")
        self.userInputLayout.addWidget(self.axonIndexTextbox)
        self.getAxonIndexButton = QtWidgets.QPushButton(self.userInputLayoutWidget)
        self.getAxonIndexButton.setObjectName("getAxonIndexButton")
        self.userInputLayout.addWidget(self.getAxonIndexButton)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Neural Image Segmentation"))
        self.label.setText(_translate("MainWindow", "  Input Image Select:"))
        self.analyzeButton.setText(_translate("MainWindow", "Analyze"))
        self.preButton.setText(_translate("MainWindow", "Gamma Correction"))
        self.pushButton.setText(_translate("MainWindow", "Segmentation"))
        self.clearButton.setText(_translate("MainWindow", "Reset"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        # self.saveButton.setText(_translate("MainWindow", "Save"))
        # self.exportButton.setText(_translate("MainWindow", "Export"))
        self.info.setText(_translate("MainWindow", "General Information:\n"))
        self.cellInfo.setText(_translate("MainWindow", "Cell Information:\n"))
        self.cellFilterLabel.setText(_translate("MainWindow", "Cell Filter Size:"))
        self.setFilterButton.setText(_translate("MainWindow", "Set Filter Size"))
        self.cellIndexLabel.setText(_translate("MainWindow", "Cell Index:"))
        self.getCellIndexButton.setText(_translate("MainWindow", "Get Cell"))
        self.axonIndexLabel.setText(_translate("MainWindow", "Axon Index:"))
        self.getAxonIndexButton.setText(_translate("MainWindow", "Highlight Axon"))
