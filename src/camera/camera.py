# Camera picture-taking class
# author: Michael Rakowiecki

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
from datetime import datetime
import cv2
import cv2.aruco as aruco
import numpy as np

class Camera:

    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(1920, 1080))
        # warmup the camera
        time.sleep(2)

    def cap_image():
        image = camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        dtime = datetime.now()
        logging.debug("Captured Image @ "+"%d-%d-%d-%d %d:%d:%d", dtime.year, 
            dtime.month, dtime.day, dtime.hour, dtime.minute, dtime.second)
        return image, dtime

    def vid_stream():
        start_time = datetime.now()
        for frame in camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = np.array(frame.array)
            # show the frame
            cv2.imshow("Farm Location", image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        end_time = datetime.now()
        time_passed_str,_ = calculate_time_passed(start_time, end_time)
        logging.debug("Video stream lasted", time_passed_str, "long")

    def calculate_time_passed(datetime start, datetime end):
        time_passed = end - start_time
        
        time_str =  time_passed.year, "year(s),",
                    time_passed.month, "month(s),", 
                    time_passed.day, "day(s),", 
                    time_passed.hour, "hour(s),", 
                    time_passed.minute, "minute(s), and", 
                    time_passed.second, "second(s)" 
        
        return time_str, time_passed      

def main() -> None:
    path = os.path.dirname(os.path.abspath(__file__))
    img_folder = os.path.join(path, "images")
    cam = Camera()
    for idx in range(0,10):
        im, time = cam.cap_image()
        cv2.imwrite(img_folder + str(idx) + "__" + str(time) + ".png", im)
    
    cam.vid_stream()

if __name__ == "__main__":
    main()