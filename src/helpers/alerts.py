'''
Module containing text and email notification classes for alerts.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

import json
import os
import logging
import smtplib
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailAlert:
    '''
    Class for sending and creating email messages.
        email_info - Dictionary containing configuration info (login credentials, etc.)
    '''
    def __init__(self, email_info: dict):
        self._username = email_info['username']
        self._password = email_info['password']
        self._smtp = email_info['smtp']
        self._port = int(email_info['port'])

    def send(self, context: dict, recipients: list):
        '''
        Send an HTML-formatted email over SMTP.
            context - Dictionary containing the contents of the message
            recipients - List of email addresses to send the email to
        '''
        # Create secure session with Gmail's SMTP server
        server = smtplib.SMTP(self._smtp, self._port)
        server.starttls()
        server.login(self._username, self._password)

        email = generate_email(context)

        try:
            response = server.sendmail(self._username, recipients, email.as_bytes())
            if response:
                print(response)
                # logging.debug(response)
        except Exception as e:
            print(e)
            # logging.error(e)
        finally:
            server.quit()


class TextAlert:
    '''
    Class for sending and creating text messages.
        twilio_info - Dictionary containing configuration info (login credentials, etc.)
    '''
    def __init__(self, twilio_info):
        self._account_SID = twilio_info['account_SID']
        self._auth_token = twilio_info['auth_token']
        self._number = twilio_info['sending_number']

    def send(self, message: str, recipients: list):
        '''
        Send a text message over SMS.
            message - String containing the contents of the message
            recipients - List of phone numbers to send the text to
        '''
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
                    logging.debug(response)
            except Exception as e:
                logging.error(e)


def generate_text(content: str) -> str:
    '''
    Generate a text based on a template with a simple prompt.
        content - String containing the message
    '''
    return (
        'An alert was triggered with message:\n\n'
        '{}\n\n'
        'This is an automated message; please do not reply.'
    ).format(content)

def generate_email(context: dict) -> MIMEMultipart:
    '''
    Generate an email based on an HTML template with a simple prompt.
        content - Dictionary containing message contents
    '''
    # Create message container and header
    email = MIMEMultipart('alternative')
    email['Subject'] = 'Sensor Data Report'

    # Create HTML email contents
    template = env.get_template('report.html')
    html = template.render(context)

    text = MIMEText(html, 'html')
    email.attach(text)

    graphs = context.get('graphs')
    if graphs:
        for graph in graphs:
            with open(graph, 'rb') as fi:
                img = MIMEImage(fi.read())
                name = os.path.basename(graph)
                img.add_header('Content-ID', '<{}>'.format(name))
                img.add_header('Content-Disposition', 'inline', filename=name)
                email.attach(img)

    return email
