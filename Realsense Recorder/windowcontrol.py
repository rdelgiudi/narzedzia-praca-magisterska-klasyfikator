from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import typing, datetime

import windowview, recordlogic

import cv2

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(object, object, float, float)

    def __init__(self, window, parent: typing.Optional['QObject'] = ...) -> None:
        super().__init__()
        self.window = window

    def run(self):
        recordlogic.recording(self)
        self.finished.emit()

class MainDialog(QMainWindow, windowview.Ui_MainWindow):

    def __init__(self, app, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(QSize(1045,680))
        self.app = app

        self.startButton.clicked.connect(self.startClicked)
        self.switchSourceButton.clicked.connect(self.switchSourceClicked)
        self.resolutionBox.currentIndexChanged.connect(self.resolutionBoxChanged)
        self.disparityShiftBox.valueChanged.connect(self.disparityShiftBoxChanged)

        self.isRecording = False
        self.showDepth = False
        self.disparityShift = 0
        self.dim = (640, 480)
    
    def closeEvent(self, a0: QCloseEvent) -> None:

        self.isRecording = False

        return super().closeEvent(a0)
    
    def startClicked(self):
        if not self.isRecording:
            self.isRecording = True
            self.startButton.setText("Stop")
            #Thread(target=recordlogic.recording, args=(self,)).start()

            self.thread = QThread()
            self.worker = Worker(window=self)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateUi)
            self.thread.start()
            
            #recordlogic.recording(self)
        else:
            self.isRecording = False
            self.startButton.setText("Start")
    
    def switchSourceClicked(self):
        if not self.showDepth:
            self.showDepth = True
            self.switchSourceButton.setText("Depth")
        else:
            self.showDepth = False
            self.switchSourceButton.setText("Color")

    def resolutionBoxChanged(self):
        match self.resolutionBox.currentIndex():
            case 0:
                self.dim = (640, 480)
            case 1:
                self.dim = (1280, 720)

    def disparityShiftBoxChanged(self):
        self.disparityShift = self.disparityShiftBox.value()

    def updateUi(self, depth_image_8U, color_image, fps, totalseconds):

        if self.showDepth:
            qtimg = depth_image_8U
            height, width = qtimg.shape
            bytesPerLine = width
            qImg = QImage(qtimg.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        else:
            qtimg = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            height, width, channel = qtimg.shape
            bytesPerLine = 3 * width
            qImg = QImage(qtimg.data, width, height, bytesPerLine, QImage.Format_RGB888)

        pixmap01 = QPixmap.fromImage(qImg)

        self.viewLabel.setPixmap(pixmap01.scaled(960, 540, Qt.KeepAspectRatio))

        self.fpsValLabel.setText("{:.2f}".format(fps))
        self.timeValLabel.setText(str(datetime.timedelta(seconds=totalseconds)))
