import dropbox
import os

dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))

def download_file(filename, savehere):
  filename= filename[1:]
  filename = "/tundra" + filename
  
  
  dbx.files_download_to_file(savehere, filename)

  


def upload_file(filename, localfile):
  filename = filename[1:]
  filename = "/tundra" + filename
  
  with open(localfile, "rb") as f:
    dbx.files_upload(f.read(), filename, mode=dropbox.files.WriteMode.overwrite)
