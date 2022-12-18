import pyrealsense2.pyrealsense2 as rs
import numpy as np
import datetime
from PyQt5 import QtGui
import cv2
from threading import Thread
import queue
from multiprocessing import Process, Queue

def updateUi(window, depth_image_8U, color_image, fps, totalseconds):

    if window.showDepth:
        qtimg = depth_image_8U
        height, width = qtimg.shape
        bytesPerLine = width
        qImg = QtGui.QImage(qtimg.data, width, height, bytesPerLine, QtGui.QImage.Format_Grayscale8)
    else:
        qtimg = color_image
        height, width, channel = qtimg.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(qtimg.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

    pixmap01 = QtGui.QPixmap.fromImage(qImg)

    window.viewLabel.setPixmap(pixmap01)

    window.fpsValLabel.setText("{:.2f}".format(fps))
    window.timeValLabel.setText(str(datetime.timedelta(seconds=totalseconds)))

def processWQueue(colorwqueue, depthwqueue, dims):

    dateandtime = datetime.datetime.today().isoformat(timespec="seconds") 

    color_path = "videos/{}_rgb.avi".format(dateandtime)
    depth_path = "videos/{}_depth.avi".format(dateandtime)
    colorwriter = cv2.VideoWriter(color_path, cv2.VideoWriter_fourcc(*"XVID"), 30, dims, 1)
    depthwriter = cv2.VideoWriter(depth_path, cv2.VideoWriter_fourcc(*"XVID"), 30, dims, 0)

    while True:
        if colorwqueue.empty() and depthwqueue.empty():
                continue
        colordata = colorwqueue.get()
        depthdata = depthwqueue.get()
        if colordata == "DONE" and depthdata == "DONE":
            break

        depthwriter.write(depthdata)
        colorwriter.write(colordata)
        

def recording(worker):
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    dims = worker.window.dim

    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.depth, dims[0], dims[1], rs.format.z16, 30)
    config.enable_stream(rs.stream.color, dims[0], dims[1], rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    align_to = rs.stream.color
    align = rs.align(align_to)

    framenum = 0
    fps = 0
    starttime = datetime.datetime.now()
    fpstime = starttime

    capturetimes = []
    aligntimes = []
    numpytimes = []
    #writetimes = []
    #updateuitimes = []

    colorwqueue = Queue()
    depthwqueue = Queue()

    writethread = Process(target=processWQueue, args=(colorwqueue, depthwqueue, dims))
    writethread.start()

    try:
        while worker.window.isRecording:
            
            #if not worker.window.isRecording:
            #    break
            
            if (datetime.datetime.now()-fpstime).total_seconds() > 5:
                framenum = 0
                fpstime = datetime.datetime.now()

            # Wait for a coherent pair of frames: depth and color
            capturestart = datetime.datetime.now()
            frames = pipeline.wait_for_frames()

            capturened = datetime.datetime.now()
            capturetimes.append((capturened - capturestart).total_seconds())

            alignstart = datetime.datetime.now()
            aligned_frames = align.process(frames)
            alignend = datetime.datetime.now()
            aligntimes.append((alignend - alignstart).total_seconds())
            
            #depth_frame = frames.get_depth_frame()
            #color_frame = frames.get_color_frame()
            #if not depth_frame or not color_frame:
            #    continue

            # Convert images to numpy array
            #depth_image = np.asanyarray(depth_frame.get_data())
            #color_image = np.asanyarray(color_frame.get_data())
            
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            
            if not aligned_depth_frame or not color_frame:
                continue
            
            numpystart = datetime.datetime.now()
            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_image_8U = cv2.convertScaleAbs(depth_image, alpha=0.03)
            numpyend = datetime.datetime.now()
            numpytimes.append((numpyend - numpystart).total_seconds())
        
            #writestart = datetime.datetime.now()
            #colorwriter.write(color_image)
            #depthwriter.write(depth_image_8U)
            colorwqueue.put(color_image)
            depthwqueue.put(depth_image_8U)
            #writeend = datetime.datetime.now()
            #writetimes.append((writeend - writestart).total_seconds())

            #updateuistart = datetime.datetime.now()
            framenum += 1
            currenttime = datetime.datetime.now()
            totalseconds = (currenttime - starttime).total_seconds()
            fpsseconds = (currenttime - fpstime).total_seconds()
            fps = framenum / fpsseconds

            #Thread(target=updateUi, args=(window, depth_image_8U, color_image, fps, totalseconds)).start()
            #updateUi(window, depth_image_8U, color_image, fps, totalseconds)
            worker.progress.emit(depth_image_8U, color_image, fps, totalseconds)
            #updateuiend = datetime.datetime.now()    # Wait for the reader and writer threads to exit
            #updateuitimes.append((updateuiend - updateuistart).total_seconds())

    finally:
        # Stop streaming
        pipeline.stop()

        print("Waiting for writing process to finish...")
        
        colorwqueue.put("DONE")
        depthwqueue.put("DONE")
        writethread.join()

        print("FPS: {:.2f}".format(fps))
        print("Operation Times:")
        captureavg = sum(capturetimes) / len(capturetimes)
        alignavg = sum(aligntimes) / len(aligntimes)
        numpyavg = sum(numpytimes) / len(numpytimes)
        #writeavg = sum(writetimes) / len(writetimes)
        #updateuiavg = sum(updateuitimes) / len(updateuitimes)

        print("Capture {} ms".format(captureavg * 1000))
        print("Align: {} ms".format(alignavg * 1000))
        print("Numpy: {} ms".format(numpyavg * 1000))
        #print("Write: {} ms".format(writeavg * 1000))
        #print("Update UI: {} ms".format(updateuiavg * 1000))

        

