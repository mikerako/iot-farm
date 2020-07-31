# Camera picture-taking class
# author: Michael Rakowiecki

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
from datetime import datetime
import logging
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

    def cap_image(self):
        # image = self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        # dtime = datetime.now()
        # logging.debug("Captured Image @ "+"%d-%d-%d-%d %d:%d:%d", dtime.year, 
        #     dtime.month, dtime.day, dtime.hour, dtime.minute, dtime.second)
        # return image, dtime
        self.camera.start_preview()
        self.camera.capture('/home/pi/Desktop/image_test.jpg')
        self.camera.stop_preview()

    def vid_stream(self):
        self.camera.resolution = (640, 480)
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        start_time = datetime.now()
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = np.array(frame.array)
            # show the frame
            cv2.imshow("Farm Location", image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        end_time = datetime.now()
        time_passed_str = self.format_time(end_time - start_time)
        logging.debug("Video stream lasted", time_passed_str)
        print("Video stream lasted", time_passed_str)
        self.rawCapture = PiRGBArray(self.camera, size=(1920, 1080))

    def format_time(self, time: datetime):
        tot_sec = time.total_seconds()
        days = tot_sec // 86400
        tot_sec -= 86400*days
        hours = tot_sec // 3600
        tot_sec -= 3600*hours
        mins = tot_sec // 60
        tot_sec -= 60*mins
        secs = tot_sec

        print("days", days)
        print("hours", hours)
        print("minuts", mins)
        print("seconds", secs)

        time_str = days, "day(s),", hours, "hour(s),", mins, "minute(s), and", secs, "second(s)"
        
        return time_str 

def main() -> None:
    path = os.path.dirname(os.path.abspath(__file__))
    img_folder = os.path.join(path, "images")
    cam = Camera()
    for idx in range(0,10):
        cam.cap_image()
        # im, time = cam.cap_image()
        # cv2.imwrite(img_folder + str(idx) + "__" + str(time) + ".png", im)
    
    cam.vid_stream()

if __name__ == "__main__":
    main()