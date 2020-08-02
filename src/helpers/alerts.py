'''
Module for handling text and email alerts.

Author: Kevin Kraydich
'''

import json
import os
import logging
import smtplib
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Logging and config files
# logging.basicConfig(filename='output.log',level=logging.DEBUG)


'''Class for sending and creating email messages.'''
class EmailAlert:
    def __init__(self, email_info: dict):
        self._username = email_info['username']
        self._password = email_info['password']
        self._smtp = email_info['smtp']
        self._port = int(email_info['port'])

    def send(self, message: str, recipients: list):
        # Create secure session with Gmail's SMTP server
        server = smtplib.SMTP(self._smtp, self._port)
        server.starttls()
        server.login(self._username, self._password)

        email = generate_email(message)

        try: 
            response = server.sendmail(self._username, recipients, email.as_string())
            if response:
                pass
                logging.debug('Could not send email to: {}'.format(response))
        except Exception as e:
            logging.error(e)
        finally:
            server.quit()


'''Class for sending and creating text messages.'''
class TextAlert:
    def __init__(self, twilio_info):
        self._account_SID = twilio_info['account_SID']
        self._auth_token = twilio_info['auth_token']
        self._number = twilio_info['sending_number']

    def send(self, message: str, recipients: list):
        client = Client(self._account_SID, self._auth_token)

        for recipient in recipients:
            full_message = generate_text(message)
            try:
                response = client.messages.create(
                    body = full_message,
                    from_ = self._number,
                    to = recipient
                )
                if response['error_code'] != 'null':
                    print(response)
            except Exception as e:
                logging.error(e)


def generate_text(content: str) -> str:
    return (
        'An alert was triggered with message:\n\n'
        '{}\n\n'
        'This is an automated message; please do not reply.'
    ).format(content)

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
