import streamlit as st
from home_page import home_page
from about_page import about_page
from feedback_page import feedback_page
from datasetmanagement_page import dataset_management_page
<<<<<<< HEAD
import logging
from dropbox_utils import DropboxLogger
from token_file import DROPBOX_ACCESS_TOKEN
dropbox_logger = DropboxLogger(DROPBOX_ACCESS_TOKEN)
=======


>>>>>>> 49773d361d4ec389ad35e455248a911b697ce76a
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append(title)  # Store only the title

    def run(self):
        st.set_page_config(page_title="AquaticRig", layout="wide")

        st.sidebar.markdown("## Main Menu")
        selected_app = st.sidebar.selectbox(
            "Select Page", self.apps
        )
        st.sidebar.markdown("---")
        try:
         if selected_app == "Home Page":
            home_page()
         elif selected_app == "Dataset Management":
            dataset_management_page()
         elif selected_app == "About Page":
            about_page()
         elif selected_app == "Feedback":
            feedback_page()

        except Exception as e:
          error_log = f"An error occurred in {selected_app}: {str(e)}"
          logging.error(error_log)
          st.error(f"An error occurred: {str(e)}")
          dropbox_logger.upload_error_log(error_log)




if __name__ == "__main__":
    app = MultiApp()

    app.add_app("Home Page", home_page)
    app.add_app("Dataset Management", dataset_management_page)
    app.add_app("About Page", about_page)
    app.add_app("Feedback", feedback_page)

    app.run()
