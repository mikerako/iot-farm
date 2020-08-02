from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json


class Uploader:
    def __init__(self, drive_info: dict):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(drive_info['credentials'])
        self._drive = GoogleDrive(gauth)
        self._parent_id = drive_info['parent_folder']
        
    def upload_file(self, filename: str, parent_id = None) -> None:
        metadata = {}

        if parent_id:
            metadata['parents'] = [
                {
                    "kind": "drive#fileLink",
                    "id": parent_id
                }
            ]

        fi = self._drive.CreateFile(metadata)
        fi.SetContentFile(filename)
        fi.Upload()
    
    def create_folder(self, filename: str):
        metadata = {
            'title': filename,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [
                {
                    "kind": "drive#fileLink",
                    "id": self._parent_id
                }
            ]
        }
        
        folder = self._drive.CreateFile(metadata)
        folder.Upload()

        return str(folder['id'])

# def main():
#     up = Uploader()
#     folder_id = up.create_folder('2020_08_01')
#     up.upload_file('hello.txt', folder_id)

# if __name__ == "__main__":
#     main()
