from helpers import alerts, user
import json
import os

# Assumes the system's current directory is iot-farm/src
with open('config.json') as f:
    CONFIG = json.load(f)

def main():
    users = user.Users(CONFIG['alerts']['users'])
    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    email.send({'date': "Hello World!"}, users.get_emails())

if __name__ == '__main__':
    main()