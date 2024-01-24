import streamlit as st
from home_page import home_page
from about_page import about_page
from feedback_page import feedback_page
from datasetmanagement_page import datasetmanagement_page
import streamlit.components.v1 as components

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

        if selected_app == "Home Page":
            home_page()
        elif selected_app == "Dataset Management":
            datasetmanagement_page()
        elif selected_app == "About Page":
            about_page()
        elif selected_app == "Feedback":
            feedback_page()


if __name__ == "__main__":
    app = MultiApp()

    app.add_app("Home Page", home_page)
    app.add_app("Dataset Management", datasetmanagement_page)
    app.add_app("About Page", about_page)
    app.add_app("Feedback", feedback_page)


    app.run()
