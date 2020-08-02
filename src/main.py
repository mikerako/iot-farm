from helpers import alerts, upload, user
import json


with open('config.json') as f:
    CONFIG = json.load(f)


def main():
    users = user.UserList(CONFIG['alerts']['users'])
    text = alerts.TextAlert(CONFIG['alerts']['twilio'])
    email = alerts.EmailAlert(CONFIG['alerts']['email'])
    uploader = upload.Uploader(CONFIG['upload'])

    # text.send('test', users.get_numbers())
    # email.send('test', users.get_emails())

    # folder_id = up.create_folder('2020_08_01')
    # up.upload_file('hello.txt', folder_id)

if __name__ == "__main__":
    main()
