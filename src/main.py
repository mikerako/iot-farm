'''
Driver code for IoT farm back-end.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

from helpers import alerts, upload, user, csv, sensor, camera
import logging
import json
import schedule
import time
import os

# Assumes the system's current directory is iot-farm/src
os.chdir('../')
SOURCE_PATH = os.path.join(os.getcwd(), 'src')
DATA_PATH = os.path.join(os.getcwd(), 'data')
LOG_PATH = os.path.join(os.getcwd(), 'log')
logging.basicConfig(level=logging.INFO, filename=os.path.join(LOG_PATH, '{}.log'.format(time.strftime('%Y_%m_%d'))))

with open(os.path.join(SOURCE_PATH, 'config-kevin.json')) as f:
    CONFIG = json.load(f)

def job_read(sensors: list, files: list) -> None:
    for i in range(len(sensors)):
        data = sensors[i].read_bme()
        line = '{},{},{},{}\n'.format(
            data['timestamp'],
            data['temperature'],
            data['humidity'],
            data['pressure'],
        )
        f = open(files[i], 'a')
        f.write(line)
        f.close()
    logging.info('Completed a sensor read job')

def job_text() -> None:
    # TODO - finish
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])
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

def job_picture():
    # TODO - finish
    pass

def job_vid_stream():
    # TODO - finish
    pass

def job_upload(files: list) -> None:
    up = upload.Uploader(CONFIG['upload'])
    folder_name = time.strftime('%Y_%m_%d')
    folder_id = up.create_folder(folder_name)

    for fi in files:
        up.upload_file(fi, parent_id=folder_id)
        reset_file(fi)
    logging.info('Completed an upload job')

def get_filename(i: int) -> str:
    return 'data_{}.csv'.format(i)

def reset_file(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)

    f = open(path, 'a')
    f.write('timestamp,temperature,humidity,pressure\n')
    f.close()
    logging.info('Reset {}'.format(path))

def main():
    users = user.Users(CONFIG['alerts']['users'])
    sensors = [sensor.EnvComboSensor(0)]
    csv_files = [os.path.join(DATA_PATH, get_filename(i)) for i in range(len(sensors))]
    cam = camera.Camera()

    for f in csv_files:
        reset_file(f)

    schedule.every(10).seconds.do(job_read, sensors=sensors, files=csv_files)
    # schedule.every().day.at("23:55").do(job_email, recipients=users.get_emails())
    schedule.every(30).seconds.do(job_email, recipients=users.get_emails())
    # schedule.every().day.at("23:59").do(job_upload, files=csv_files)
    schedule.every(30).seconds.do(job_upload, files=csv_files)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.debug(e)

if __name__ == "__main__":
    main()
