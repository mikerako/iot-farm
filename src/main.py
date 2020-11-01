'''
Driver code for IoT farm backend.

Authors:
Kevin Kraydich <kevin.kraydich@gmail.com>
Michael Rakowiecki <kevin.kraydich@gmail.com>
'''

from helpers import alerts, upload, user, csv, sensor, camera
import logging
import json
import schedule
import datetime
import time
import cv2
import os

# Assumes the system's current directory is iot-farm/src, so move to iot-farm
SOURCE_PATH = os.path.join(os.getcwd(), '../src')
DATA_PATH = os.path.join(os.getcwd(), '../data')
LOG_PATH = os.path.join(os.getcwd(), '../log')

# Open logging file inside log/
logging.basicConfig(level=logging.INFO, filename=os.path.join(LOG_PATH, '{}.log'.format(time.strftime('%Y_%m_%d'))))
last_notification_time = None

# Open private config files
with open(os.path.join(SOURCE_PATH, 'config-kevin.json')) as f:
    CONFIG = json.load(f)

# Returns true if the current time is within the interval that
# the lights are on, false otherwise.
def are_lights_on() -> bool:
    current = datetime.datetime.now().time()
    start = current.replace(7, 0, 0)
    end = current.replace(12 + 6, 0, 0)
    return start <= current <= end

# Checks to see when the last text notification was sent out. This
# is to prevent sending too many texts at one time. Returns true if
# we have not sent a text in a while, otherwise it returns false.
def check_last_notification(time: time) -> bool:
    return not last_notification_time or time <= last_notification_time + datetime.timedelta(hours=8)

# Checks a sensor reading for any values outside of the given min and
# max thresholds. Returns a string containing an appropriate message if
# any values are outside the thresholds, otherwise return an empty string.
def alert_threshold(reading: dict, thresholds: dict):
    msg = ''
    for key in thresholds.keys():
        min_threshold, max_threshold = thresholds[key]
        if reading[key] < min_threshold:
            msg += format_text(key, reading[key], True)
        elif reading[key] > max_threshold:
            msg += format_text(key, reading[key], False)
    return msg

# Formats a message based on whether the reading was too high or too low.
# Returns a string containing the formatted message.
def format_text(measurement: str, value: float, is_low: bool) -> str:
    status = 'low' if is_low else 'high'
    rounded = round(value, 2)
    return '{} too {} (value = {})\n'.format(measurement, status, rounded)

# Returns a properly formatted filename given an index
def get_filename(i: int) -> str:
    return 'data_{}.csv'.format(i)

# Given a filename, resets the sensor file values.
def reset_file(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)

    f = open(path, 'a')
    f.write('timestamp,temperature,humidity,pressure\n')
    f.close()
    logging.info('Reset {}'.format(path))

# Sends a text alert to all listed users if a sensor value is outside the defined thresholds
def send_text_alert(recipients: list, reading: dict, thresholds: dict) -> None:
    now = datetime.datetime.now()
    msg = alert_threshold(reading, thresholds)
    # Check when the last notification was sent
    if check_last_notification(datetime.datetime.now()) and msg:
        # Update the time of last notification sent
        last_notification_time = now
        # Send the message to all users
        job_text(recipients, msg)

def job_read(recipients: list, sensors: list, files: list, thresholds: dict) -> None:
    average = {
        'timestamp': 0,
        'temperature': 0,
        'humidity': 0,
        'pressure': 0
    }
    num_sensors_read = 0
    # Read the current values from all sensors
    for i in range(len(sensors)):
        data = sensors[i].read_bme()

        # Update the running average
        for key in data.keys():
            average[key] = (data[key] + num_sensors_read * average[key]) / (num_sensors_read + 1)
        num_sensors_read += 1

        # Write the results to the appropriate file
        line = '{},{},{},{}\n'.format(
            data['timestamp'],
            data['temperature'],
            data['humidity'],
            data['pressure'],
        )
        f = open(files[i], 'a')
        f.write(line)
        f.close()

    send_text_alert(recipients, average, thresholds)
    logging.info('Completed a sensor read job')

def job_text(recipients: list, message: str) -> None:
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])
    text.send(message, recipients)
    logging.info('Completed a text job')

def job_email(recipients: list) -> None:
    # file_paths = [os.path.join(DATA_PATH, get_filename(i) for i in range(num_sensors)]
    file_path = os.path.join(DATA_PATH, get_filename(0))
    csv_processor = csv.CSVProcessor(DATA_PATH, file_path)

    context = {
        'date': time.strftime('%A, %B %d'),
        'graphs': csv_processor.make_graphs()
    }

    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    email.send(context, recipients)
    logging.info('Completed an email job')    

def job_picture(camera):
    img = camera.cap_image()
    cv2.imwrite(DATA_PATH + time.strftime('%Y_%m_%d') + ".png", img)

def job_upload(files: list) -> None:
    up = upload.Uploader(CONFIG['upload'])
    folder_name = time.strftime('%Y_%m_%d')
    folder_id = up.create_folder(folder_name)

    for fi in files:
        up.upload_file(fi, parent_id=folder_id)
        reset_file(fi)

    logging.info('Completed an upload job')

def main():
    users = user.Users(CONFIG['alerts']['users'])
    sensors = [sensor.EnvComboSensor(0)]
    csv_files = [os.path.join(DATA_PATH, get_filename(i)) for i in range(len(sensors))]
    cam = camera.Camera()
    thresholds = {
        'temperature': (58, 85),
        'humidity': (0, 100),
    }

    for f in csv_files:
        reset_file(f)

    schedule.every(10).seconds.do(
        job_read, recipients=users.get_numbers(), sensors=sensors, files=csv_files, thresholds=thresholds
    )
    schedule.every(30).seconds.do(job_picture, camera=cam)
    # schedule.every().day.at("23:55").do(job_email, recipients=users.get_emails())
    schedule.every(30).seconds.do(job_email, recipients=users.get_emails())
    # schedule.every().day.at("21:18").do(job_upload, files=csv_files)
    schedule.every(30).seconds.do(job_upload, files=csv_files)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.debug(e)

if __name__ == "__main__":
    main()
