'''Module for handling text and email alerts.'''
import json
import os
import logging
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logging.basicConfig(filename='error.log',level=logging.DEBUG)
CONFIG_FILENAME = 'config.json'

class User:
    def __init__(self, params):
        self.name = params['name']
        self.number = params['number']
        self.email = params['email']

class EmailAlert:
    def __init__(self, sender):
        self._sender = sender

    def send(self, message):
        

    def generate_email(self, name, report):
        return (
            '<p><strong>Hi {}! Here is the daily report:</strong></p>'
            '<p>{}</p>'
            '<p><strong>This is an automated message; please do not reply.</strong></p>'
        ).format(name, report)


class TextAlert:
    def __init__(self):
        with open(CONFIG_FILENAME) as f:
            config = json.load(f)

        account_SID = config['twilio']['account_SID']
        auth_token = config['twilio']['auth_token']

        self._client = Client(account_SID, auth_token)
        self._number = config['twilio']['sending_number']
        self._users = []

        for user_params in config['users']:
            if validate_number(user_params['number']):
                new_user = User(user_params)
                self._users.append(new_user)
            else:
                logging.error(
                    'Improper formatting of user with name {}'.format(
                        user_params['name']
                    )
                )

    def send(self, message):
        for user in self._users:
            full_message = generate_message(user.name, message)
            try:
                self._client.messages.create(
                    body = full_message,
                    from_ = self._number,
                    to = user.number
                )
            except:
                logging.error('Could not send message to {}'.format(user))

def generate_message(name, body):
    return (
        'Hi {}! An alert was triggered with message:\n\n'
        '{}\n\n'
        'This is an automated message; please do not reply.'
    ).format(name, body)

def validate_number(num):
    return len(num) == 12 and num[0] == '+'
