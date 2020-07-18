# Camera picture-taking class
# author: Michael Rakowiecki

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import cv2.aruco as aruco
import numpy as np

class Camera:

    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(camera, size=(640, 480))
        # warmup the camera
        time.sleep(2)

    def cap_image():
        image = camera.capture(rawCapture, format="bgr", use_video_port=True)
        print("Captured Image")
        return image

    def vid_stream():
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = np.array(frame.array)
            # show the frame
            cv2.imshow("Farm Location", image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            