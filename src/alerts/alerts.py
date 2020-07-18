'''Module for handling text and email alerts.'''
import json
import os
import re
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

logging.basicConfig(filename='error.log',level=logging.DEBUG)
CONFIG_FILENAME = 'CONFIG.json'
with open(CONFIG_FILENAME) as f:
    CONFIG = json.load(f)

class User:
    def __init__(self, params):
        self.name = params['name']
        self.number = params['number']
        self.email = params['email']

class UserList:
    def __init__(self):
        self.users = []
        self.add_users(CONFIG['users'])
    
    def add_user(self, user_info):
        if self.validate(user_info):
            self.users.append(User(user_info))
    
    def add_users(self, users):
        for user_params in users:
            if self.validate(user_params):
                new_user = User(user_params)
                self.users.append(new_user)

    def get_users(self):
        return self.users
    
    def validate(self, user_info):
        res = validate_number(user_info['number']) and validate_email(user_info['email'])
        return res

class EmailAlert:
    def __init__(self, users):
        api_key = CONFIG['sendgrid']['api_key']
        self._client = SendGridAPIClient(api_key=api_key)
        self._email = CONFIG['email']
        self._users = users.get_users()

    def send(self, message):
        for user in self._users:
            email = Mail(
                    from_email = self._email,
                    to_emails = user.email,
                    subject = 'Sensor Data Report',
                    html_content = generate_message(user.name, message, False)
            )
            try: 
                response = self._client.send(email)
                for msg in [response.status_code, response.body, response.headers]:
                    print(msg)
                    logging.debug(msg)
            except Exception as e:
                print('email didnt work')
                print(e)
                logging.error(e)

class TextAlert:
    def __init__(self, users):
        account_SID = CONFIG['twilio']['account_SID']
        auth_token = CONFIG['twilio']['auth_token']

        self._client = Client(account_SID, auth_token)
        self._number = CONFIG['twilio']['sending_number']
        self._users = users.get_list()

    def send(self, message):
        for user in self._users:
            full_message = generate_message(user.name, message, True)
            try:
                self._client.messages.create(
                    body = full_message,
                    from_ = self._number,
                    to = user.number
                )
            except:
                logging.error('Could not send message to {}'.format(user))

def generate_message(name, body, isPlaintext):
    if isPlaintext:
        return (
            'Hi {}! An alert was triggered with message:\n\n'
            '{}\n\n'
            'This is an automated message; please do not reply.'
        ).format(name, body)
    return (
            '<p><strong>Hi {}! Here is the daily report:</strong></p>'
            '<p>{}</p>'
            '<p><strong>This is an automated message; please do not reply.</strong></p>'
        ).format(name, body)

def validate_number(num):
    return re.match(r'^\+[1-9]\d{1,14}$', num) is not None

def validate_email(email):    
    regexp = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return re.match(regexp, email) is not None

users = UserList()
email = EmailAlert(users)
email.send('test')

# text = TextAlert()
# text.send('test')
