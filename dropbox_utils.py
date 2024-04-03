import dropbox
from token_file import DROPBOX_ACCESS_TOKEN
import streamlit as st
from datetime import datetime
import datetime
class DropboxLogger:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

    def upload_file(self, file_data, file_name, st):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # Construct the new filename with the user's email
            new_file_name = f"feedback_report_{current_time}.pdf"

            # Upload the file to Dropbox
            upload_path = f'/Apps/Feedbackfiles/{new_file_name}'
            self.dbx.files_upload(file_data, upload_path, mode=dropbox.files.WriteMode.overwrite)

            st.success(f"Feedback PDF '{new_file_name}' uploaded successfully to Dropbox.")
        except dropbox.exceptions.ApiError as e:
            st.error(f"Error uploading '{file_name}' to Dropbox: {e}")


    def upload_error_log(self, error_log):
        # Format the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Download the existing error log file from Dropbox
        try:
            _, existing_file = self.dbx.files_download('/Apps/Feedbackfiles/error_log.txt')
            existing_error_log = existing_file.content.decode('utf-8')
        except dropbox.exceptions.ApiError:
            existing_error_log = ""

        # Append the new error log with timestamp to the existing content
        updated_error_log = existing_error_log + f"\n{current_time} - {error_log}"

        # Upload the updated error log back to Dropbox
        with open('updated_error_log.txt', 'w') as f:
            f.write(updated_error_log)

        with open('updated_error_log.txt', 'rb') as f:
            try:
                self.dbx.files_upload(f.read(), '/Apps/Feedbackfiles/error_log.txt',
                                      mode=dropbox.files.WriteMode.overwrite)
                print("Error log updated and uploaded successfully to Dropbox.")
            except dropbox.exceptions.ApiError as e:
                print(f"Error updating error log on Dropbox: {e}")