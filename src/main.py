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

def job_read(sensors: list) -> None:
    for i in range(len(sensors)):
        sensor = sensors[i]
        data = sensor.read_bme()
        line = '{},{},{},{}'.format(
            data['timestamp'],
            data['temperature'],
            data['humidity'],
            data['pressure'],
        )

        f = open(get_filename(i), 'a')
        f.write(line)
        f.close()

def job_text():
    # TODO - finish
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])

def job_email(recipients: list):
    csv_processor = csv.CSVProcessor('data/random.csv')

    context = {
        'date': time.strftime('%A, %B %d'),
        'graphs': csv_processor.make_graphs()
    }

    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    email.send(context, recipients)

def job_upload():
    up = upload.Uploader(CONFIG['upload'])
    folder_name = time.strftime('%Y_%m_%d')
    folder_id = up.create_folder(folder_name)

    for filename in os.listdir('data'):
        if filename.endswith('.csv'):
            full_path = os.path.join('data', filename)
            up.upload_file(full_path, folder_id)
            reset_file(full_path)

def get_filename(i: int) -> str:
    return 'data_{}.csv'.format(i)

def reset_file(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
    
    f = open(path, 'a')
    f.write('timestamp,temperature,humidity,pressure')
    f.close()

def main():
    users = user.Users(CONFIG['alerts']['users'])
    sensors = [sensor.EnvComboSensor(0)]

    for i in range(len(sensors)):
        filename = get_filename(i)
        full_path = os.path.join('data', filename)
        reset_file(full_path)

    # TODO - add scheduled tasks
    schedule.every().day.at('23:55').do(job_upload)
    schedule.every().day.at('08:30').do(job_email, recipients=users.get_emails())
    schedule.every(1).seconds.do(job_read, sensors=sensors)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
