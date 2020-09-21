'''
Driver code for IoT farm back-end.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

from helpers import alerts, upload, user, csv, sensor
import json
import schedule
import time
import os

with open('config.json') as f:
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
    print('read the sensor!')

def job_text() -> None:
    # TODO - finish
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])

def job_email(recipients: list) -> None:
    csv_processor = csv.CSVProcessor('data/data_0.csv')

    context = {
        'date': time.strftime('%A, %B %d'),
        'graphs': csv_processor.make_graphs()
    }

    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    email.send(context, recipients)
    print('emailed people!')

def job_upload(files: list) -> None:
    up = upload.Uploader(CONFIG['upload'])
    folder_name = time.strftime('%Y_%m_%d')
    folder_id = up.create_folder(folder_name)

    for fi in files:
        up.upload_file(fi, folder_id)
        reset_file(fi)
    print('uploaded!') 

def get_filename(i: int) -> str:
    return 'data_{}.csv'.format(i)

def reset_file(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
    
    f = open(path, 'a')
    f.write('timestamp,temperature,humidity,pressure\n')
    f.close()

def main():
    users = user.Users(CONFIG['alerts']['users'])
    sensors = [sensor.EnvComboSensor(0)]
    csv_files = [os.path.join('data', get_filename(i)) for i in range(len(sensors))]

    for f in csv_files:
        reset_file(f)

    # TODO - add scheduled tasks
    # schedule.every().day.at('23:55').do(job_upload)
    schedule.every(1).seconds.do(job_read, sensors=sensors, files=csv_files)
    # schedule.every().day.at('08:30').do(job_email, recipients=users.get_emails())
    schedule.every(15).seconds.do(job_email, recipients=users.get_emails())
    schedule.every(20).seconds.do(job_upload, files=csv_files)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
