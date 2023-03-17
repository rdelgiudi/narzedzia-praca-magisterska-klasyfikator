from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtTest

import windowview
import cv2, os
import numpy as np
import time, typing


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(QPixmap, int)

    def __init__(self, window, parent: typing.Optional['QObject'] = ...) -> None:
        super().__init__()
        self.window = window

    def run(self):
        while (self.window.running):
            self.window.capture_frame()
            QtTest.QTest.qWait(int(1000/self.window.fps))

        self.finished.emit()

class MainDialog(QMainWindow, windowview.Ui_MainWindow):

    def __init__(self, app, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.app = app

        self.cutButton.clicked.connect(self.cutClicked)
        self.quitButton.clicked.connect(self.quitClicked)
        self.videoSlider.sliderMoved.connect(self.sliderMoved)
        self.videoSlider.sliderReleased.connect(self.sliderReleased)
        self.openButton.clicked.connect(self.openClicked)
        self.startButton.clicked.connect(self.startClicked)

        self.video_path = None
        self.worker = None
        self.running = False

    def sliderMoved(self, value):
        if not self.running:
            self.frameLabel.setText(f"Frame: {value}")
    
    def sliderReleased(self):
        if not self.running:
            val = self.videoSlider.value()
            self.video.set(cv2.CAP_PROP_POS_FRAMES, val-1)
            self.capture_frame()
    
    def capture_frame(self):
        if self.video is not None:
            ret, frame = self.video.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                current_frame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))

                if self.worker is not None:
                    self.worker.progress.emit(pixmap, current_frame)
                else:
                    self.videoLabel.setPixmap(pixmap.scaled(self.videoLabel.width(), self.videoLabel.height(), Qt.KeepAspectRatio))
                    self.videoSlider.setValue(current_frame)
                    self.frameLabel.setText(f"Frame: {current_frame}")
            else:
                self.startClicked()

    
    def quitClicked(self):
        self.video.release()
        self.close()

    def cutClicked(self):
        if self.video is not None:
            frame_number = self.videoSlider.value()
            frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

            # Ensure that the selected frame is not within the 5 frames at the start or end of the video
            if frame_number >= 5 and frame_number <= (frame_count - 6):
                # Set the start and end frames for the cut
                start_frame = frame_number - 5
                end_frame = frame_number + 5

                # Create a directory for the cut frames with the name "frame_X"
                output_dir = os.path.join(os.getcwd(), f"frame_{frame_number}")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Create a NumPy array to store the cut frames
                frames = np.zeros((11, int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), 3), dtype=np.uint8)

                # Iterate through the frames and write the cut frames as images and to the NumPy array
                self.video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                for i in range(start_frame, end_frame+1):
                    ret, frame = self.video.read()
                    if ret:
                        # Save the frame as an image
                        output_filename = os.path.join(output_dir, f"frame_{i}.jpg")
                        cv2.imwrite(output_filename, frame)

                        # Save the frame to the NumPy array
                        frames[i-start_frame] = frame
                    else:
                        break

                # Save the NumPy array to a .npy file
                np.save(os.path.join(output_dir, f"frames.npy"), frames)

                # Show a success message
                QMessageBox.information(self, "Frame Cut Successful", f"The cut frames were saved to {output_dir} and to {os.path.join(output_dir, 'frames.npy')}.")
            else:
                QMessageBox.warning(self, "Invalid Frame Selection", "Please select a frame that is at least 5 frames away from the start or end of the video.")

    def openClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Select Video File", "","Video Files (*.mp4 *.avi *.mkv)", options=options)
        if file_name: 
            self.video_path = file_name
            self.video = cv2.VideoCapture(self.video_path)
            self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
            total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.videoSlider.setMaximum(total_frames)
            self.videoSlider.setMinimum(1)
            self.capture_frame()
        
    def startClicked(self):
        if (self.running):
            self.running = False
            self.worker = None
            self.startButton.setText("Start")

        else:
            self.running = True
            self.startButton.setText("Pause")

            self.thread = QThread()
            self.worker = Worker(window=self)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.updateUi)
            self.thread.start()
    
    def updateUi(self, pixmap, current_frame):

        self.videoLabel.setPixmap(pixmap.scaled(self.videoLabel.width(), self.videoLabel.height(), Qt.KeepAspectRatio))
        self.videoSlider.setValue(current_frame)
        self.frameLabel.setText(f"Frame: {current_frame}")