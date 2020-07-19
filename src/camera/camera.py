# Camera picture-taking class
# author: Michael Rakowiecki

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
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
        time_passed = calculate_time_passed(start_time, end_time)
        logging.debug("Video stream lasted", time_passed, "long")

    def calculate_time_passed(datetime start, datetime end):
        years_passed = end.year - start.year
        months_passed = end.month - start.month
        days_passed = end.day - start.day
        hours_passed = end.hour - start.hour
        minutes_passed = end.minute - start.minute
        seconds_passed = end.second - start.second
        
        xtra_days = 0
        leap_yr_count = 0
        curr_month = start.month
        curr_year = start.year
        while(curr_month != end.month && curr_year <= end.year):
            if(curr_month == 1):
                xtra_days += 31
            if(curr_month == 2):
                if(curr_year % 4 == 0 && curr_year % 100 != 0):
                    xtra_days += 29
                    leap_yr_count += 1
                else:
                    xtra_days += 28
            if(curr_month == 3):
                xtra_days += 31
            if(curr_month == 4):
                xtra_days += 30
            if(curr_month == 5):
                xtra_days += 31
            if(curr_month == 6):
                xtra_days += 30
            if(curr_month == 7):
                xtra_days += 31
            if(curr_month == 8):
                xtra_days += 31
            if(curr_month == 9):
                xtra_days += 30
            if(curr_month == 10):
                xtra_days += 31
            if(curr_month == 11):
                xtra_days += 30
            if(curr_month == 12):
                xtra_days += 31
                curr_year += 1
            
            curr_month += 1
             
        total_seconds = seconds_passed + 60*minutes_passed + 3600*hours_passed + 
                     86400*days_passed + xtra_days

        time_gone = {"year(s)": years_passed}
        total_seconds -= (years_passed * (365*86400) + 86400*leap_yr_count)
        time_gone["month(s)"] = months_passed
        total_seconds -= (xtra_days)
        time_gone["day(s)"] = total_seconds % 86400
        total_seconds -= time_gone["day(s)"] * 86400
        time_gone["hour(s)"] = total_seconds % 3600
        total_seconds -= time_gone["hour(s)"] * 3600
        time_gone["minute(s)"] = minutes_passed
        total_seconds -= time_gone["minute(s)"] * 60
        time_gone["second(s)"] = total_seconds
        
        return time_gone            