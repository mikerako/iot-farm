from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

CONFIG_FILE = 'my_creds.txt'

class Uploader:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(CONFIG_FILE)
        self._drive = GoogleDrive(gauth)
        
    def upload_file(self, filename: str) -> None:
        fi = self._drive.CreateFile()
        fi.SetContentFile(filename)
        fi.Upload()

def main():
    up = Uploader()
    up.upload_file('hello.txt')

if __name__ == "__main__":
    main()
