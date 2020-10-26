from helpers import upload
import json
import os

# Assumes the system's current directory is iot-farm/src
with open('config.json') as f:
    CONFIG = json.load(f)

def create_file(filename: str):
    f = open(filename, 'w')
    f.write('Hello world!')
    f.close()

def main():
    uploader = upload.Uploader(CONFIG['upload'])
    filename = 'test.txt'
    create_file(filename)
    try:
        uploader.upload_file(filename)
    except Exception as e:
        print(e)
    finally:
        os.remove(filename)

if __name__ == '__main__':
    main()