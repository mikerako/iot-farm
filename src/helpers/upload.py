'''
Module that interfaces with Google Drive for uploading files and creating folders.

Author: Kevin Kraydich <kevin.kraydich@gmail.com>
'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import os

class Uploader:
    '''
    Class that interfaces with Google Drive.
        drive_info - Dictionary containing configuration info (login credentials, etc.)
    '''
    def __init__(self, drive_info: dict):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(drive_info['credentials'])
        self._drive = GoogleDrive(gauth)
        self._parent_id = drive_info['parent_folder']

    def upload_file(self, filename: str, parent_id = None) -> None:
        '''
        Upload a file to Google Drive.
            filename - The name of the file to upload
            parent_id - The ID of the new file's parent directory; by default, this is the root directory.
        '''
        metadata = {}

        if parent_id:
            metadata['parents'] = [
                {
                    "kind": "drive#fileLink",
                    "id": parent_id,
                }
            ]

        fi = self._drive.CreateFile(metadata)
        fi['title'] = os.path.basename(filename)
        fi.SetContentFile(filename)
        fi.Upload()

    def create_folder(self, filename: str):
        '''
        Creates a folder in Google Drive. Returns the ID of the newly created folder.
            filename - Name of the folder to be created
        '''
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
