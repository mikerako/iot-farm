'''
Driver code for IoT farm back-end.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

from helpers import alerts, upload, user, csv
import json
import schedule
import time

with open('config.json') as f:
    CONFIG = json.load(f)

def job_email(recipients: list):
    csv_processor = csv.CSVProcessor('data/random.csv')

    context = {
        'date': time.strftime('%A, %B %d'),
        'graphs': csv_processor.make_graphs()
    }

    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    email.send(context, recipients)

def job_text():
    # TODO - finish
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])

def job_upload():
    up = upload.Uploader(CONFIG['upload'])
    folder_name = time.strftime('%Y_%m_%d')
    folder_id = up.create_folder(folder_name)
    up.upload_file('data/random.csv', folder_id)

    # TODO - delete files after they've been uploaded to Google Drive

def main():
    users = user.Users(CONFIG['alerts']['users'])

    # TODO - add scheduled tasks
    schedule.every().day.at('00:00').do(job_upload)
    schedule.every().day.at('8:30').do(job_email, recipients=users.get_emails())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
