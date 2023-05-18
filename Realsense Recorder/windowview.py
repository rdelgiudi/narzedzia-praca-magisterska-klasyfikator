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
        MainWindow.resize(1045, 680)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(910, 620, 88, 34))
        self.startButton.setObjectName("startButton")
        self.viewLabel = QtWidgets.QLabel(self.centralwidget)
        self.viewLabel.setGeometry(QtCore.QRect(40, 20, 960, 540))
        self.viewLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.viewLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.viewLabel.setText("")
        self.viewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.viewLabel.setObjectName("viewLabel")
        self.switchSourceButton = QtWidgets.QPushButton(self.centralwidget)
        self.switchSourceButton.setGeometry(QtCore.QRect(800, 620, 88, 34))
        self.switchSourceButton.setObjectName("switchSourceButton")
        self.fpsLabel = QtWidgets.QLabel(self.centralwidget)
        self.fpsLabel.setGeometry(QtCore.QRect(10, 620, 41, 18))
        self.fpsLabel.setObjectName("fpsLabel")
        self.fpsValLabel = QtWidgets.QLabel(self.centralwidget)
        self.fpsValLabel.setGeometry(QtCore.QRect(50, 620, 58, 18))
        self.fpsValLabel.setObjectName("fpsValLabel")
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(10, 640, 41, 16))
        self.timeLabel.setObjectName("timeLabel")
        self.timeValLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeValLabel.setGeometry(QtCore.QRect(50, 640, 111, 18))
        self.timeValLabel.setObjectName("timeValLabel")
        self.resolutionLabel = QtWidgets.QLabel(self.centralwidget)
        self.resolutionLabel.setGeometry(QtCore.QRect(630, 620, 81, 31))
        self.resolutionLabel.setObjectName("resolutionLabel")
        self.resolutionBox = QtWidgets.QComboBox(self.centralwidget)
        self.resolutionBox.setGeometry(QtCore.QRect(710, 620, 61, 31))
        self.resolutionBox.setObjectName("resolutionBox")
        self.resolutionBox.addItem("")
        self.resolutionBox.addItem("")
        self.resolutionLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.resolutionLabel_2.setGeometry(QtCore.QRect(430, 620, 91, 31))
        self.resolutionLabel_2.setObjectName("resolutionLabel_2")
        self.disparityShiftBox = QtWidgets.QSpinBox(self.centralwidget)
        self.disparityShiftBox.setGeometry(QtCore.QRect(520, 620, 71, 31))
        self.disparityShiftBox.setMaximum(200)
        self.disparityShiftBox.setObjectName("disparityShiftBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RealSense Recorder"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.switchSourceButton.setText(_translate("MainWindow", "Color"))
        self.fpsLabel.setText(_translate("MainWindow", "FPS:"))
        self.fpsValLabel.setText(_translate("MainWindow", "0"))
        self.timeLabel.setText(_translate("MainWindow", "Time:"))
        self.timeValLabel.setText(_translate("MainWindow", "0:0:0"))
        self.resolutionLabel.setText(_translate("MainWindow", "Resolution:"))
        self.resolutionBox.setItemText(0, _translate("MainWindow", "480p"))
        self.resolutionBox.setItemText(1, _translate("MainWindow", "720p"))
        self.resolutionLabel_2.setText(_translate("MainWindow", "Disparity Shift:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
