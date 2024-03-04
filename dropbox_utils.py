import dropbox
from token_file import DROPBOX_ACCESS_TOKEN

class DropboxLogger:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

    def upload_error_log(self, error_log):
        with open('error_log.txt', 'w') as f:
            f.write(error_log)

        with open('error_log.txt', 'rb') as f:
            self.dbx.files_upload(f.read(), '/path/to/error_log.txt', mode=dropbox.files.WriteMode.overwrite)
