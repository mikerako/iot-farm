'''Module for handling text and email alerts.'''
import json
import os
import re
import logging
import smtplib
from twilio.rest import Client
from email.message import EmailMessage

# Logging and config files
logging.basicConfig(filename='output.log',level=logging.DEBUG)
CONFIG_FILENAME = 'CONFIG.json'
with open(CONFIG_FILENAME) as f:
    CONFIG = json.load(f)

'''Class for storing name, number, and email address.'''
class User:
    def __init__(self, params):
        self.name = params['name']
        self.number = params['number']
        self.email = params['email']

'''Class for storing and accessing valid user data.'''
class UserList:
    def __init__(self):
        self.users = []
        self.add_users(CONFIG['users'])
    
    def add_user(self, user_info):
        if self.validate(user_info):
            self.users.append(User(user_info))
        else:
            logging.debug('Improper formatting of user with name {}'.format(user_info['name']))
    
    def add_users(self, users):
        for user_params in users:
            self.add_user(user_params)

    def get_users(self):
        return self.users
    
    def validate(self, user_info):
        res = validate_number(user_info['number']) and validate_email(user_info['email'])
        return res

'''Class for sending and creating email messages.'''
class EmailAlert:
    def __init__(self, users):
        self._users = users.get_users()
        self._username = CONFIG['email']['username']
        self._password = CONFIG['email']['password']

    def send(self, message):
        # Create secure session with Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self._username, self._password)

        # Send email to every user
        for user in self._users:
            email = generate_email(self._username, user, message)
            try: 
                response = server.send_message(email)
                if response:
                    logging.debug(response)
            except Exception as e:
                logging.error(e)
        
        server.quit()

'''Class for sending and creating text messages.'''
class TextAlert:
    def __init__(self, users):
        self._account_SID = CONFIG['twilio']['account_SID']
        self._auth_token = CONFIG['twilio']['auth_token']
        self._number = CONFIG['twilio']['sending_number']
        self._users = users.get_list()

    def send(self, message):
        client = Client(self._account_SID, self._auth_token)

        for user in self._users:
            full_message = generate_text(user.name, message)
            try:
                client.messages.create(
                    body = full_message,
                    from_ = self._number,
                    to = user.number
                )
            except Exception as e:
                logging.error(e)

def generate_text(name, content):
    return (
        'Hi {}! An alert was triggered with message:\n\n'
        '{}\n\n'
        'This is an automated message; please do not reply.'
    ).format(name, content)

def generate_email(from_email, to_user, content):
    body = (
        '<p><strong>Hi {}! Here is the daily report:</strong></p>'
        '<div id="report">{}</div>'
        '<p><strong>This is an automated message; please do not reply.</strong></p>'
    ).format(to_user.name, content)

    email = EmailMessage()
    email['Subject'] = 'Sensor Data Report'
    email['From'] = from_email
    email.set_content(body)
    email['To'] = to_user.email

    return email

def validate_number(num):
    return re.match(r'^\+[1-9]\d{1,14}$', num) is not None

def validate_email(email):    
    regexp = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return re.match(regexp, email) is not None

def main():
    # Get list of users
    users = UserList()

    # Send a test email
    email = EmailAlert(users)
    email.send('test')

    # Send a test text
    # text = TextAlert()
    # text.send('test')

if __name__ == "__main__":
    main()
