'''Module for handling text and email alerts.'''
import json
import os
import re
import logging
import smtplib
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Logging and config files
logging.basicConfig(filename='output.log',level=logging.DEBUG)
CONFIG_FILENAME = 'CONFIG.json'
with open(CONFIG_FILENAME) as f:
    CONFIG = json.load(f)


'''Class for storing name, number, and email address.'''
class User:
    def __init__(self, params: dict):
        self.name = params['name']
        self.number = params['number']
        self.email = params['email']


'''Class for storing and accessing valid user data.'''
class UserList:
    def __init__(self):
        self.users = []
        self.add_users(CONFIG['users'])
    
    def add_user(self, user_info: dict):
        if self.validate(user_info):
            self.users.append(User(user_info))
        else:
            logging.error('Improper formatting of user with name {}'.format(user_info['name']))
    
    def add_users(self, users: list):
        for user_params in users:
            self.add_user(user_params)

    def get_users(self) -> list:
        return self.users
    
    def validate(self, user_info: dict) -> bool:
        res = validate_number(user_info['number']) and validate_email(user_info['email'])
        return res


'''Class for sending and creating email messages.'''
class EmailAlert:
    def __init__(self, users: UserList):
        email_info = CONFIG['email']
        self._username = email_info['username']
        self._password = email_info['password']
        self._smtp = email_info['smtp']
        self._port = int(email_info['port'])
        self._users = users.get_users()

    def send(self, message: str):
        # Create secure session with Gmail's SMTP server
        server = smtplib.SMTP(self._smtp, self._port)
        server.starttls()
        server.login(self._username, self._password)

        email = generate_email(message)
        recipients = [user.email for user in self._users]

        try: 
            response = server.sendmail(self._username, recipients, email.as_string())
            if response:
                logging.debug('Could not send email to: {}'.format(response))
        except Exception as e:
            logging.error(e)
        finally:
            server.quit()


'''Class for sending and creating text messages.'''
class TextAlert:
    def __init__(self, users: UserList):
        self._account_SID = CONFIG['twilio']['account_SID']
        self._auth_token = CONFIG['twilio']['auth_token']
        self._number = CONFIG['twilio']['sending_number']
        self._users = users.get_users()

    def send(self, message: str):
        client = Client(self._account_SID, self._auth_token)

        for user in self._users:
            full_message = generate_text(user.name, message)
            try:
                response = client.messages.create(
                    body = full_message,
                    from_ = self._number,
                    to = user.number
                )
                if response['error_code'] != 'null':
                    logging.debug(response)
            except Exception as e:
                logging.error(e)


def generate_text(name: str, content: str) -> str:
    return (
        'Hi {}! An alert was triggered with message:\n\n'
        '{}\n\n'
        'This is an automated message; please do not reply.'
    ).format(name, content)

def generate_email(content: str) -> MIMEMultipart:
    # Create message container and header
    email = MIMEMultipart('alternative')
    email['Subject'] = 'Sensor Data Report'

    # Create HTML email contents
    html = (
        '<html>'
        '<head></head>'
        '<body>'
        '<p><strong>Here is the daily report:</strong></p>'
        '<div id="report">{}</div>'
        '<p><strong>This is an automated message; please do not reply.</strong></p>'
        '</body>'
        '</html>'
    ).format(content)

    text = MIMEText(html, 'html')
    email.attach(text)

    return email

def validate_number(phone_number: str) -> bool:
    regexp = r'^\+[1-9]\d{1,14}$'
    return re.match(regexp, phone_number) is not None

def validate_email(email: str) -> bool:    
    regexp = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return re.match(regexp, email) is not None

def main():
    # Get list of users
    users = UserList()

    # Send an email
    email = EmailAlert(users)
    email.send('test')

    # Send a text
    text = TextAlert(users)
    text.send('test')

if __name__ == "__main__":
    main()
