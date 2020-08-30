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

def email(recipients: list):
    csv_processor = csv.CSVProcessor('data/random.csv')

    context = {
        'date': time.strftime('%A, %B %d'),
        'graphs': csv_processor.make_graphs()
    }

    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    email.send(context, recipients)

def text():
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])

def job():
    # Create users, text/email alerts, and uploader objects
    uploader = upload.Uploader(CONFIG['upload'])

    # text.send('test', users.get_numbers())
    # email.send('test', users.get_emails())

    # folder_id = up.create_folder('2020_08_01')
    # up.upload_file('hello.txt', folder_id)

def main():
    users = user.Users(CONFIG['alerts']['users'])

    # TODO - add scheduled tasks
    schedule.every().day.at('8:30').do(email, recipients=users.get_emails())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
