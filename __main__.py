import sys
import os
import numpy as np
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QIcon, QPixmap
from DAIDetector import DAIdetector
from ExcelOut import ExcelPrinter

import cv2 as cv
import time 

class Ui_MainWindow(object):
    
    def __init__(self):
        self.fstProbability = 50 # First cascade probability value
        self.secProbability = 50 # Second cascade probability value
        self.detectionModel = DAIdetector(fstProb = self.fstProbability, secProb = self.secProbability)
        self.outputResolution = (500,500)
        self.workStatus = False
        self.saveFolder = 'res/output'
        self.imgStream = None
        self.fileName = None # Will hold the image address location
        self.origTmp = None # Original image
        self.procTmp = None # Proccesed image
        self.camPort = 0 # Camera port
        pass
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 631, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.showStack = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.showStack.setContentsMargins(0, 0, 0, 0)
        self.showStack.setObjectName("showStack")
        self.ImageOutputTabs = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.ImageOutputTabs.setObjectName("ImageOutputTabs")
        self.origTab = QtWidgets.QWidget()
        self.origTab.setMinimumSize(QtCore.QSize(500, 500))
        self.origTab.setObjectName("origTab")
        self.origImg = QtWidgets.QLabel(self.origTab)
        self.origImg.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.origImg.setFrameShape(QtWidgets.QFrame.Box)
        self.origImg.setFrameShadow(QtWidgets.QFrame.Plain)
        self.origImg.setText("")
        self.origImg.setObjectName("origImg")
        self.ImageOutputTabs.addTab(self.origTab, "")
        self.procTab = QtWidgets.QWidget()
        self.procTab.setObjectName("procTab")
        self.procImg = QtWidgets.QLabel(self.procTab)
        self.procImg.setGeometry(QtCore.QRect(0, 0, 500, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.procImg.sizePolicy().hasHeightForWidth())
        self.procImg.setSizePolicy(sizePolicy)
        self.procImg.setFrameShape(QtWidgets.QFrame.Box)
        self.procImg.setFrameShadow(QtWidgets.QFrame.Plain)
        self.procImg.setText("")
        self.procImg.setTextFormat(QtCore.Qt.AutoText)
        self.procImg.setAlignment(QtCore.Qt.AlignCenter)
        self.procImg.setWordWrap(False)
        self.procImg.setObjectName("procImg")
        self.ImageOutputTabs.addTab(self.procTab, "")
        self.showStack.addWidget(self.ImageOutputTabs)
        self.InputStreamTabs = QtWidgets.QTabWidget(self.centralwidget)
        self.InputStreamTabs.setGeometry(QtCore.QRect(640, 179, 160, 301))
        self.InputStreamTabs.setObjectName("InputStreamTabs")
        self.file = QtWidgets.QWidget()
        self.file.setObjectName("file")
        self.fileImputButton = QtWidgets.QPushButton(self.file)
        self.fileImputButton.setGeometry(QtCore.QRect(0, 10, 150, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileImputButton.sizePolicy().hasHeightForWidth())
        self.fileImputButton.setSizePolicy(sizePolicy)
        self.fileImputButton.setObjectName("fileImputButton")
        self.InputStreamTabs.addTab(self.file, "")
        self.cam = QtWidgets.QWidget()
        self.cam.setObjectName("cam")
        self.cameraPort = QtWidgets.QComboBox(self.cam)
        self.cameraPort.setGeometry(QtCore.QRect(10, 10, 130, 22))
        self.cameraPort.setObjectName("cameraPort")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.cameraPort.addItem("")
        self.InputStreamTabs.addTab(self.cam, "")
        self.Text = QtWidgets.QLabel(self.centralwidget)
        self.Text.setGeometry(QtCore.QRect(640, 0, 160, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Text.setFont(font)
        self.Text.setAlignment(QtCore.Qt.AlignCenter)
        self.Text.setObjectName("Text")
        self.probabilitySliderFirst = QtWidgets.QSlider(self.centralwidget)
        self.probabilitySliderFirst.setGeometry(QtCore.QRect(640, 60, 151, 22))
        self.probabilitySliderFirst.setMinimum(1)
        self.probabilitySliderFirst.setProperty("value", 50)
        self.probabilitySliderFirst.setOrientation(QtCore.Qt.Horizontal)
        self.probabilitySliderFirst.setObjectName("probabilitySliderFirst")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(640, 480, 160, 30))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(640, 510, 160, 30))
        self.stopButton.setObjectName("stopButton")
        self.fileOutputButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileOutputButton.setGeometry(QtCore.QRect(640, 140, 150, 28))
        self.fileOutputButton.setObjectName("fileOutputButton")
        self.probabilitySliderSecond = QtWidgets.QSlider(self.centralwidget)
        self.probabilitySliderSecond.setGeometry(QtCore.QRect(640, 110, 151, 22))
        self.probabilitySliderSecond.setMinimum(1)
        self.probabilitySliderSecond.setProperty("value", 50)
        self.probabilitySliderSecond.setOrientation(QtCore.Qt.Horizontal)
        self.probabilitySliderSecond.setObjectName("probabilitySliderSecond")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(640, 40, 150, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(640, 90, 141, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.ImageOutputTabs.setCurrentIndex(0)
        self.InputStreamTabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.add_functions()
        self.reset()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DAI detector"))
        self.ImageOutputTabs.setTabText(self.ImageOutputTabs.indexOf(self.origTab), _translate("MainWindow", "Original Image"))
        self.ImageOutputTabs.setTabText(self.ImageOutputTabs.indexOf(self.procTab), _translate("MainWindow", "Proccesed Image"))
        self.fileImputButton.setText(_translate("MainWindow", "Input File"))
        self.InputStreamTabs.setTabText(self.InputStreamTabs.indexOf(self.file), _translate("MainWindow", "File"))
        self.cameraPort.setItemText(0, _translate("MainWindow", "1"))
        self.cameraPort.setItemText(1, _translate("MainWindow", "2"))
        self.cameraPort.setItemText(2, _translate("MainWindow", "3"))
        self.cameraPort.setItemText(3, _translate("MainWindow", "4"))
        self.cameraPort.setItemText(4, _translate("MainWindow", "5"))
        self.cameraPort.setItemText(5, _translate("MainWindow", "6"))
        self.cameraPort.setItemText(6, _translate("MainWindow", "7"))
        self.cameraPort.setItemText(7, _translate("MainWindow", "8"))
        self.cameraPort.setItemText(8, _translate("MainWindow", "9"))
        self.cameraPort.setItemText(9, _translate("MainWindow", "10"))
        self.InputStreamTabs.setTabText(self.InputStreamTabs.indexOf(self.cam), _translate("MainWindow", "Camera"))
        self.Text.setText(_translate("MainWindow", "Min % probability"))
        self.startButton.setText(_translate("MainWindow", "START"))
        self.stopButton.setText(_translate("MainWindow", "STOP"))
        self.fileOutputButton.setText(_translate("MainWindow", "Output File"))
        self.label.setText(_translate("MainWindow", "First cascade: 50"))
        self.label_2.setText(_translate("MainWindow", "Second cascade: 50"))


    def reset(self):
        self.fstProbability = 50 # First cascade probability value
        self.secProbability = 50 # Second cascade probability value
        self.detectionModel = DAIdetector(fstProb = self.fstProbability, secProb = self.secProbability)
        self.outputResolution = (500,500)
        self.workStatus = False
        self.saveFolder = 'res/output'
        self.imgStream = None
        self.fileName = None # Will hold the image address location
        self.origTmp = None # Original image
        self.procTmp = None # Proccesed image
        self.camPort = 0 # Camera port
    
    def add_functions(self):
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.fileImputButton.clicked.connect(self.loadVideo)
        self.fileOutputButton.clicked.connect(self.setSaveFolder)
        self.probabilitySliderFirst.valueChanged['int'].connect(self.firstProbValue)
        self.probabilitySliderSecond.valueChanged['int'].connect(self.secondProbValue)
        
    def erMessage(self, winName, erText):
        msg = QMessageBox()
        msg.setWindowTitle(winName)
        msg.setText(erText)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def start(self):   
        output = ExcelPrinter(directory = self.saveFolder)
        output.newfile()
        frame_num = 0
        start_time = time.time()
        fps = 0
        self.workStatus = True
        try:
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            vidout = cv.VideoWriter('{0}/{1}.mp4'.format(self.saveFolder, 'Proccesed video'),
                                    fourcc, 20.0, (500, 500))

            er = 0
            while (self.imgStream.isOpened()):  
                ret, frame = self.imgStream.read()  
                if type(frame) != type(np.array([])):
                    if er > 3:
                        break
                    er += 1
                    print("broken frame")
                    continue

                image, DAI, DAIcoord, alpha, DAIimgSet = self.detectionModel.detectDAI(frame, inputType = "array")

                end_time = time.time()
                fps = fps * 0.9 + 1/(end_time - start_time) * 0.1
                start_time = end_time
                # Draw additional info
                image = cv.resize(image, (500,500))
                frame_info = 'Frame: {0}, FPS: {1:.2f}'.format(frame_num, fps)
                cv.putText(image, frame_info, (10, image.shape[0]-10),
                            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                outImage = self.multiStack(DAIimgSet)
                self.setOrigFrame(image)
                self.setProcFrame(outImage)

                print(DAI, DAIcoord, alpha)
                if len(DAIcoord) != 0:
                    output.addObservation(DAI, DAIcoord, alpha)
                vidout.write(cv.flip(cv.flip(outImage,0), 0))

                key = cv.waitKey(1) & 0xFF

                # Exit
                if not self.workStatus:
                    break

                # Take screenshot
                if key == ord('s'):
                    cv.imwrite('{0}/frame_{1}.jpg'.format(self.saveFolder, time.time()), frame)

                frame_num += 1
            print('Done')
        except BaseException:
            self.erMessage('Error', str(BaseException))
        else:
            self.erMessage('working status', 'Computations complete')
        finally:
            self.workStatus = False
            self.imgStream.release()
            vidout.release()
    
    def stop(self):
        self.workStatus = False
        pass
        
    def loadVideo(self):
        file = QFileDialog.getOpenFileName(filter="Video (*.*)")[0]
        if not os.path.exists(file):
            raise IOError('Can\'t open "{0}"'.format(file))
        self.imgStream = cv.VideoCapture(file)
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        #self.video = cv.imread(self.fileName)
        print('File choosen: {0}'.format(file))
        self.update()

    def setOrigFrame(self,image):
        self.origTmp = image
        image = cv.resize(image, (500, 500))
        frame = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.origImg.setPixmap(QtGui.QPixmap.fromImage(image))

    def setProcFrame(self,image):
        self.procTmp = image
        image = cv.resize(image, (500, 500))
        frame = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.procImg.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def setSaveFolder(self):
        self.saveFolder = QFileDialog.getExistingDirectory()
        print('Image saved in: {0}'.format(self.saveFolder))
        
    def firstProbValue(self, value):
        self.fstProbability = value
        print('First cascade probability: ',value)
        self.update()
        
    def secondProbValue(self, value):
        self.secProbability = value
        print('Second cascade probability: ',value)
        self.update()
    
    def update(self):
        self.label.setText("First cascade: {0}".format(self.fstProbability))
        self.label_2.setText("Second cascade: {0}".format(self.secProbability))
        if self.workStatus == True:
            self.detectionModel.fstProb = self.fstProbability 
            self.detectionModel.secProb = self.secProbability
        #self.setProcFrame(img)
        #self.setOrigFrame(img2)
        pass
    
    def multiStack(self, imgArray):
        rows =  math.ceil(len(imgArray) ** 0.5)
        delta = rows * rows - len(imgArray)
        print("{0} of {1} used".format(len(imgArray), rows))
        imgStack = []

        if isinstance(imgArray, list):
            if len(imgArray) == 0:
                gray_level = 127
                gray_image = gray_level * np.ones((self.outputResolution[0], self.outputResolution[1], 3), dtype = np.uint8)
                return gray_image
            for x in range(0, rows):
                result = []
                for y in range(0, rows):
                    if x * rows + y < len(imgArray):
                        resized = cv.resize(imgArray[x * rows + y], 
                                            (round(self.outputResolution[0]/rows),round(self.outputResolution[1]/rows)))
                        result.append(resized)
                    else:
                        gray_level = 127
                        gray_image = gray_level * np.ones((round(
                            self.outputResolution[0]/rows),round(self.outputResolution[1]/rows),3), dtype = np.uint8)
                        result.append(gray_image)
                imgStack.append(np.hstack(result))
            return np.vstack(imgStack)
        else:
            assert 'Wrong Image Array type in stacking function'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())