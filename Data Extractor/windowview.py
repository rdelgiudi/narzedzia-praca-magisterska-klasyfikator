# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowview.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1224, 844)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.videoLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoLabel.setGeometry(QtCore.QRect(40, 50, 1131, 551))
        self.videoLabel.setText("")
        self.videoLabel.setObjectName("videoLabel")
        self.cutButton = QtWidgets.QPushButton(self.centralwidget)
        self.cutButton.setEnabled(False)
        self.cutButton.setGeometry(QtCore.QRect(1050, 720, 75, 23))
        self.cutButton.setObjectName("cutButton")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(1140, 720, 75, 23))
        self.quitButton.setObjectName("quitButton")
        self.frameLabel = QtWidgets.QLabel(self.centralwidget)
        self.frameLabel.setGeometry(QtCore.QRect(860, 720, 181, 21))
        self.frameLabel.setObjectName("frameLabel")
        self.videoSlider = QtWidgets.QSlider(self.centralwidget)
        self.videoSlider.setEnabled(False)
        self.videoSlider.setGeometry(QtCore.QRect(30, 710, 811, 41))
        self.videoSlider.setOrientation(QtCore.Qt.Horizontal)
        self.videoSlider.setObjectName("videoSlider")
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setEnabled(True)
        self.openButton.setGeometry(QtCore.QRect(1050, 760, 75, 23))
        self.openButton.setObjectName("openButton")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setEnabled(False)
        self.startButton.setGeometry(QtCore.QRect(260, 760, 75, 23))
        self.startButton.setObjectName("startButton")
        self.videoSpeedLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoSpeedLabel.setGeometry(QtCore.QRect(540, 760, 71, 21))
        self.videoSpeedLabel.setObjectName("videoSpeedLabel")
        self.speedSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.speedSpinBox.setGeometry(QtCore.QRect(610, 760, 62, 22))
        self.speedSpinBox.setMinimum(0.25)
        self.speedSpinBox.setMaximum(4.0)
        self.speedSpinBox.setSingleStep(0.25)
        self.speedSpinBox.setProperty("value", 1.0)
        self.speedSpinBox.setObjectName("speedSpinBox")
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setEnabled(False)
        self.nextButton.setGeometry(QtCore.QRect(350, 760, 75, 23))
        self.nextButton.setObjectName("nextButton")
        self.previousButton = QtWidgets.QPushButton(self.centralwidget)
        self.previousButton.setEnabled(False)
        self.previousButton.setGeometry(QtCore.QRect(170, 760, 75, 23))
        self.previousButton.setObjectName("previousButton")
        self.tenBackButton = QtWidgets.QPushButton(self.centralwidget)
        self.tenBackButton.setEnabled(False)
        self.tenBackButton.setGeometry(QtCore.QRect(80, 760, 75, 23))
        self.tenBackButton.setObjectName("tenBackButton")
        self.tenForwardButton = QtWidgets.QPushButton(self.centralwidget)
        self.tenForwardButton.setEnabled(False)
        self.tenForwardButton.setGeometry(QtCore.QRect(440, 760, 75, 23))
        self.tenForwardButton.setObjectName("tenForwardButton")
        self.openDepthButton = QtWidgets.QPushButton(self.centralwidget)
        self.openDepthButton.setEnabled(True)
        self.openDepthButton.setGeometry(QtCore.QRect(1140, 760, 75, 23))
        self.openDepthButton.setObjectName("openDepthButton")
        self.colorLabel = QtWidgets.QLabel(self.centralwidget)
        self.colorLabel.setGeometry(QtCore.QRect(40, 630, 861, 16))
        self.colorLabel.setObjectName("colorLabel")
        self.depthLabel = QtWidgets.QLabel(self.centralwidget)
        self.depthLabel.setGeometry(QtCore.QRect(40, 670, 861, 16))
        self.depthLabel.setObjectName("depthLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1224, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data extractor"))
        self.cutButton.setText(_translate("MainWindow", "Cut"))
        self.quitButton.setText(_translate("MainWindow", "Quit"))
        self.frameLabel.setText(_translate("MainWindow", "Frame : 0"))
        self.openButton.setText(_translate("MainWindow", "Open Color"))
        self.startButton.setText(_translate("MainWindow", "Play"))
        self.videoSpeedLabel.setText(_translate("MainWindow", "Video Speed:"))
        self.nextButton.setText(_translate("MainWindow", "Next"))
        self.previousButton.setText(_translate("MainWindow", "Previous"))
        self.tenBackButton.setText(_translate("MainWindow", "< 10"))
        self.tenForwardButton.setText(_translate("MainWindow", "10 >"))
        self.openDepthButton.setText(_translate("MainWindow", "Open Depth"))
        self.colorLabel.setText(_translate("MainWindow", "Color video loaded:"))
        self.depthLabel.setText(_translate("MainWindow", "Depth video loaded:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
