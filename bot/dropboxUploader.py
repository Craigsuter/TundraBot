import dropbox
import os

dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))

def download_file(filename, savehere):
  dbx.files_download_to_file(savehere, filename)

  


def upload_file(filename, localfile):

  with open(localfile, "rb") as f:
    dbx.files_upload(f.read(), filename, mode=dropbox.files.WriteMode.overwrite)
