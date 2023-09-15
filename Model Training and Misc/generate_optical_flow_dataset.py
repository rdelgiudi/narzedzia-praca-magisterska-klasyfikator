#https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
#https://stackoverflow.com/questions/27644388/optical-flow-using-opencv-horizontal-and-vertical-components
##################################
# Program generujący przepływ optyczny dla strumienia czasowego
# Sposób użycia: umieść program w folderze test lub train oraz uruchom
##################################

import os
import cv2
import numpy as np

for root_dir in os.listdir():
    if os.path.isdir(root_dir):
        for dirname in os.listdir(root_dir):
            dirname = os.path.join(root_dir, dirname)
            if os.path.isdir(dirname):
                print("Generating optical flow in directory: " + dirname)

                file_one = None
                file_two = None

                for imgfile in os.listdir(dirname):
                    
                    if imgfile.__contains__("000"):
                        continue

                    if file_one is None:
                        file_one = os.path.join(dirname, imgfile)
                    elif file_two is None:
                        file_two = os.path.join(dirname, imgfile)
                    
                    if file_one is not None and file_two is not None:

                        print(f"Generating optical flow for files: {file_one} and {file_two}")

                        frame1 = cv2.imread(file_one)
                        frame1 = cv2.fastNlMeansDenoisingColored(frame1,None,10,10,7,21)
                        frame2 = cv2.imread(file_two)
                        frame2 = cv2.fastNlMeansDenoisingColored(frame2,None,10,10,7,21)

                        prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                        hsv = np.zeros_like(frame1)
                        hsv[..., 1] = 255
                        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                        horz = cv2.normalize(flow[...,0], None, 0, 255, cv2.NORM_MINMAX)     
                        vert = cv2.normalize(flow[...,1], None, 0, 255, cv2.NORM_MINMAX)
                        horz = horz.astype('uint8')
                        vert = vert.astype('uint8')

                        cv2.imwrite(file_one, horz)
                        cv2.imwrite(file_two, vert)

                        file_one = None
                        file_two = None