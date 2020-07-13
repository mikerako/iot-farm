import json
import logging
from twilio.rest import Client

CONFIG_FILENAME = 'config.json'

class User:
    def __init__(self, params):
        self.name = params['name']
        self.number = params['number']

class TextAlert:
    def __init__(self):
        with open(CONFIG_FILENAME) as f:
            config = json.load(f)

        account_SID = config['account_SID']
        auth_token = config['auth_token']

        self._client = Client(account_SID, auth_token)
        self._number = config['sending_number']
        self._users = []

        for user_params in config['users']:
            new_user = User(user_params)
            self._users.append(new_user)

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
                pass

def generate_message(name, body):
    return (
        'Hi {}! An alert was triggered with message:\n\n'
        '{}\n\n'
        'This is an automated message; please do not reply.'
    ).format(name, body)

# testing purposes only
text = TextAlert()
text.send('test - remade code bc im retarded')