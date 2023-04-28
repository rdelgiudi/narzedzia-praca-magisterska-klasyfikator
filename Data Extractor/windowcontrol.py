from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtTest

import windowview
import cv2, os
import numpy as np
import time, typing

# Worker zajmujący się odczytywaniem kolejnych klatek w oddzielnym wątku
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(QPixmap, int)

    def __init__(self, window, parent: typing.Optional['QObject'] = ...) -> None:
        super().__init__()
        self.window = window

    def run(self):
        while (self.window.running):
            start = time.time()
            pixmap, current_frame = self.window.capture_frame()
            elapsed = time.time() - start
            waittime = self.window.speedframetime - elapsed
            #print(f"Capture time: {elapsed}")
            #print(f"Frametime: {self.window.speedframetime}")
            #print(f"Waittime: {waittime}")
            if waittime > 0:
                #QtTest.QTest.qWait(int(1000 * waittime))
                time.sleep(waittime)
            
            if pixmap is not None and current_frame is not None:
                self.progress.emit(pixmap, current_frame)
                self.window.app.processEvents()

        self.finished.emit()

class MainDialog(QMainWindow, windowview.Ui_MainWindow):

    def __init__(self, app, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.app = app

        self.bindButtons()

        self.video_path = None
        self.worker = None
        self.frametime = None
        self.running = False
        self.speed = 1.0

        self.video = None
        self.video_depth = None
        self.total_frames = None
        self.depth_video = None
        self.total_frames_depth = None
        self.cut_video_fragment = False
        
    # Funkcja łącząca kliknięcia guzików do odpowiednich funkcji
    def bindButtons(self):
        self.cutButton.clicked.connect(self.cutFrame)
        self.quitButton.clicked.connect(self.quitApp)
        self.videoSlider.sliderMoved.connect(self.sliderMoved)
        self.videoSlider.sliderReleased.connect(self.setFrame)
        self.openButton.clicked.connect(self.openFile)
        self.startButton.clicked.connect(self.startClicked)
        self.speedSpinBox.valueChanged.connect(self.setSpeed)
        self.nextButton.clicked.connect(self.nextFrame)
        self.previousButton.clicked.connect(self.previousFrame)
        self.tenBackButton.clicked.connect(self.previousTenFrame)
        self.tenForwardButton.clicked.connect(self.nextTenFrame)
        self.openDepthButton.clicked.connect(self.openDepthFile)

    # Funkcja dezaktywująca przyciski interfejsu
    def toggleButtonsOff(self):
        self.cutButton.setEnabled(False)
        self.videoSlider.setEnabled(False)
        self.startButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.previousButton.setEnabled(False)
        self.tenBackButton.setEnabled(False)
        self.tenForwardButton.setEnabled(False)
        self.openButton.setEnabled(False)
        self.openDepthButton.setEnabled(False)
    
    # Funkcja aktywująca przyciski interfejsu
    def toggleButtonsOn(self):
        self.cutButton.setEnabled(True)
        self.videoSlider.setEnabled(True)
        self.startButton.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.previousButton.setEnabled(True)
        self.tenBackButton.setEnabled(True)
        self.tenForwardButton.setEnabled(True)
        self.openButton.setEnabled(True)
        self.openDepthButton.setEnabled(True)
    
    # Funkcja aktualizująca label informujący o obecnej klatce
    def setFrameLabel(self, val):
        self.frameLabel.setText(f"Frame: {val} / {self.total_frames}")

    # Funkcja ustawiająca następną klatkę
    def nextFrame(self):
        if not self.running:
            self.capture_frame()
    
    # Funkcja ustawiająca klatkę o 10 wprzód
    def nextTenFrame(self):
        if not self.running:
            current_frame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
            self.video.set(cv2.CAP_PROP_POS_FRAMES, current_frame + 9)
            self.capture_frame()
    
    # Funkcja ustawiająca klatkę o 10 wstecz
    def previousTenFrame(self):
        if not self.running:
            current_frame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
            if current_frame >= 10:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 11)
                self.capture_frame()
            else:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.capture_frame()
    
    # Funkcja ustawiająca klatkę na poprzednią
    def previousFrame(self):
        if not self.running:
            current_frame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
            if current_frame >= 2:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 2)
                self.capture_frame()
            else:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.capture_frame()

    # Funkcja aktualizująca podgląd wskazywanej klatki
    def sliderMoved(self, value):
        if not self.running:
            self.setFrameLabel(value)
    
    # Funkcja ustawiająca wskazaną klatkę
    def setFrame(self):
        if not self.running:
            val = self.videoSlider.value()
            self.video.set(cv2.CAP_PROP_POS_FRAMES, val-1)
            self.capture_frame()
    
    # Funkcja aktualizująca prędkość odtwarzania
    def setSpeed(self, val):
        self.speed = val
        if self.frametime is not None:
            self.speedframetime = self.frametime / self.speed
    
    # Funkcja przechwytująca klatkę
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

                # Wysłanie klatki do procesu głównego, aby ta zaaktualizowała UI, gdy worker jest zainicjalizowany
                if self.worker is not None:
                    return pixmap, current_frame
                    #self.worker.progress.emit(pixmap, current_frame)
                else:
                    self.videoLabel.setPixmap(pixmap.scaled(self.videoLabel.width(), self.videoLabel.height(), Qt.KeepAspectRatio))
                    self.videoSlider.setValue(current_frame)
                    self.setFrameLabel(current_frame)    
            else:
                self.startClicked()
        
        return None, None

    # Funkcja wychodząca z aplikacji
    def quitApp(self):
        if self.video is not None:
            self.video.release()
        if self.video_depth is not None:
            self.video_depth.release()
        self.close()

    # Funkcja służąca wycięciu obecnie wskazywanej klatki
    def cutFrame(self):
        self.toggleButtonsOff()

        if self.video is not None:
            frame_number = self.videoSlider.value()
            frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

            # Upewnienie się, że jest wystarczająco klatek po klatce startowej
            if frame_number <= (frame_count - 121):
                # Ustawienie klatki początkowej i końcowej
                start_frame = frame_number 
                end_frame = frame_number + 120

                # Stworzenie folderu do którego wysyłane będą dane
                dateandtime = time.strftime("%Y%m%d-%H%M%S")
                output_dir = os.path.join(os.getcwd(), dateandtime + f"_frames")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                r = None
                if self.cutCheckBox.isChecked():
                    ret, frame = self.video.read()
                    if ret:
                        r = cv2.selectROI("Select cut area", frame)
                        width = int(r[2])
                        height = int(r[3])
                        cv2.destroyAllWindows()
                        self.video.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)

                print(f"[DEBUG] Cutting video frames of size {width}x{height}")

                # Tworzenie numpy array zawierającego klatki koloru + klatka głębi na początku (jeżeli wczytany jest plik głębi)
                if self.video_depth is None:
                    frames = np.zeros((120, height, width, 3), dtype=np.uint8)
                else:
                    frames = np.zeros((121, height, width, 3), dtype=np.uint8)

                    self.video_depth.set(cv2.CAP_PROP_POS_FRAMES, start_frame-1)
                    ret, frame = self.video_depth.read()

                    if ret:

                        if r is not None:
                            frame = frame[int(r[1]):int(r[1] + r[3]),
                                    int(r[0]):int(r[0] + r[2])]

                        frames[0] = frame
                        output_filename = os.path.join(output_dir, f"{dateandtime}_frame_depth.jpg")
                        cv2.imwrite(output_filename, frame)

                output_videoname = os.path.join(output_dir, f"{dateandtime}_frames.avi")
                writer = cv2.VideoWriter(output_videoname, cv2.VideoWriter_fourcc(*"XVID"), self.fps, (width, height),1)
                
                # Iterowanie przez wybrane klatki 
                self.video.set(cv2.CAP_PROP_POS_FRAMES, start_frame-1)


                print("[DEBUG] Writing frames...")
                for i in range(start_frame, end_frame):
                    ret, frame = self.video.read()

                    if r is not None:
                        frame = frame[int(r[1]):int(r[1] + r[3]),
                                        int(r[0]):int(r[0] + r[2])]

                    if ret:
                        # Zapis to filmu
                        writer.write(frame)

                        # Zapis do numpy array
                        if self.video_depth is None:
                            frames[i-start_frame] = frame
                        else:
                            frames[i-start_frame+1] = frame
                    else:
                        break

                # Zapis numpy array do pliku .npz (skompresowany)
                print("[DEBUG] Writing compressed .npz file...")
                np.savez_compressed(os.path.join(output_dir, f"{dateandtime}_frames.npz"), frames)

                print("[DEBUG] Writing completed!")

                # Informacja o powodzeniu
                QMessageBox.information(self, "Frame Cut Successful!", f"The cut frames were saved to:\n{output_dir}\n.npz file saved to:\n{os.path.join(output_dir, f'frames_{start_frame}.npz')}.")

                self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                writer.release()
            else:
                QMessageBox.warning(self, "Invalid Frame Selection!", "Please select a frame that is at least 120 frames away from the end of the video.")

            self.toggleButtonsOn()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Select Video File", "","Video Files (*.mp4 *.avi *.mkv)", options=options)
        if file_name: 
            self.video_path = file_name
            self.colorLabel.setText("Color video loaded: " + self.video_path)
            self.video = cv2.VideoCapture(self.video_path)
            self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
            print("[DEBUG] Loaded color video. Video properties:")
            print(f"FPS: {self.fps}")
            self.frametime = 1.0 / self.fps
            print(f"Frametime: {self.frametime}")
            self.speedframetime = self.frametime / self.speed
            print(f"Frametime with speed modifier: {self.speedframetime}")
            self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"Total video frames: {self.total_frames}")
            
            self.videoSlider.setMaximum(self.total_frames)
            self.videoSlider.setMinimum(1)
            self.capture_frame()

            self.toggleButtonsOn()

            if self.total_frames_depth != self.total_frames and self.total_frames_depth is not None:
                print("[DEBUG] Warning! Videos seem to not match! Check video files before cutting!")
                QMessageBox.warning(self, "Frame discrepancy detected!" ,"Warning! Videos seem to not match! Check video files before cutting!")
            if self.video_depth is not None:
                if self.video_depth.get(cv2.CAP_PROP_FRAME_HEIGHT) != self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) or self.video_depth.get(cv2.CAP_PROP_FRAME_WIDTH) != self.video.get(cv2.CAP_PROP_FRAME_WIDTH):
                    QMessageBox.warning(self, "Frame discrepancy detected!" ,"Impossble to cut from videos. Video dimensions must match!")
                    self.cutButton.setEnabled(False)
    
    def openDepthFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Select Video File", "","Video Files (*.mp4 *.avi *.mkv)", options=options)
        if file_name: 
            self.video_path_depth = file_name
            self.depthLabel.setText("Depth video loaded: " + self.video_path_depth)
            self.video_depth = cv2.VideoCapture(self.video_path_depth)
            self.fps_depth = int(self.video_depth.get(cv2.CAP_PROP_FPS))
            print("[DEBUG] Loaded depth video. Video properties:")
            print(f"FPS: {self.fps}")
            self.frametime_depth = 1.0 / self.fps_depth
            print(f"Frametime: {self.frametime_depth}")
            self.speedframetime_depth = self.frametime_depth / self.speed
            print(f"Frametime with speed modifier: {self.speedframetime_depth}")
            self.total_frames_depth = int(self.video_depth.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"Total video frames: {self.total_frames_depth}")

            self.cutButton.setEnabled(True)
            
            if self.total_frames_depth != self.total_frames and self.total_frames is not None:
                print("[DEBUG] Warning! Videos seem to not match! Check video files before cutting!")
                QMessageBox.warning(self, "Frame discrepancy detected!" ,"Warning! Videos seem to not match! Check video files before cutting!")
            if self.video is not None:
                if (self.video_depth.get(cv2.CAP_PROP_FRAME_HEIGHT) != self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) or self.video_depth.get(cv2.CAP_PROP_FRAME_WIDTH) != self.video.get(cv2.CAP_PROP_FRAME_WIDTH)):
                    QMessageBox.warning(self, "Frame discrepancy detected!" ,"Impossble to cut from videos. Video dimensions must match!")
                    self.cutButton.setEnabled(False)
        
    def startClicked(self):
        if (self.running):
            self.running = False
            self.worker = None
            self.startButton.setText("Play")

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
        self.setFrameLabel(current_frame)