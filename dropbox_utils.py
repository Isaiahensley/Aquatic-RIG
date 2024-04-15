import dropbox
from datetime import datetime
from io import BytesIO


class DropboxLogger:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)

    def upload_file(self, file_data, st):
        try:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_file_name = f"feedback_report_{current_time}.pdf"
            upload_path = f'/Apps/Feedbackfiles/{new_file_name}'
            self.dbx.files_upload(file_data, upload_path, mode=dropbox.files.WriteMode.overwrite)
            st.success(f"Feedback PDF '{new_file_name}' uploaded successfully to Dropbox.")
        except dropbox.exceptions.ApiError as e:
            st.error(f"Error uploading PDF to Dropbox: {e}")

    def upload_error_log(self, error_log):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            _, existing_file = self.dbx.files_download('/Apps/Feedbackfiles/error_log.txt')
            existing_error_log = existing_file.content.decode('utf-8')
        except dropbox.exceptions.ApiError:
            existing_error_log = ""

        updated_error_log = f"{existing_error_log}\n{current_time} - {error_log}"
        error_log_buffer = BytesIO(updated_error_log.encode('utf-8'))

        try:
            self.dbx.files_upload(error_log_buffer.getvalue(), '/Apps/Feedbackfiles/error_log.txt',
                                  mode=dropbox.files.WriteMode.overwrite)
            print("Error log updated and uploaded successfully to Dropbox.")
        except dropbox.exceptions.ApiError as e:
            print(f"Error updating error log on Dropbox: {e}")

# Usage in Streamlit, outside of the DropboxLogger
# logger = DropboxLogger('your-access-token')
# logger.upload_file(file_data, st)
