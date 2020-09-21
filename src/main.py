'''
Driver code for IoT farm back-end.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

from helpers import alerts, upload, user, csv
import json
import schedule
import time
import os

with open('config.json') as f:
    CONFIG = json.load(f)

def job_read():
    # TODO - implement
    pass

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
            os.remove(full_path)

def main():
    users = user.Users(CONFIG['alerts']['users'])

    # TODO - add scheduled tasks
    schedule.every().day.at('11:55').do(job_upload)
    schedule.every().day.at('08:30').do(job_email, recipients=users.get_emails())
    schedule.every(60).seconds.do(job_read)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
