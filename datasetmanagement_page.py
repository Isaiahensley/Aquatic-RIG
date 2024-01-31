import streamlit as st
from datetime import datetime
import netCDF4 as nc

def datasetmanagement_page():
    # Page title
    st.title("Dataset Management")

    # File uploader
    file_upload = st.file_uploader("Upload dataset", type=["nc"])

    # Options for dataset visualization
    options = st.selectbox(
        "How would you like this dataset visualized?",
        ("Scatter Plot", "Quiver", "Heat Map", "Contourf"
    ))

    # Sliders for Time and Depth
    st.slider("Time", value=datetime(2020, 1, 1, 9, 30), format="MM/DD/YY - hh:mm")
    st.slider("Depth", 0, 100)

    if file_upload is not None:
        st.text("file uploaded")
        file_content = file_upload.read()  # Read file content as bytes
        nc_file = nc.Dataset('in-memory', memory=file_content, diskless=True)

        # Get and display information about the dataset
        st.text(f"Number of variables: {len(nc_file.variables)}")
        st.text(f"Variables: {list(nc_file.variables.keys())}")











    # Depending on the option selected, the corresponding graph should be used on the dataset and displayed
    # on the website

#def scatterplot(file, time, depth):
    #code here

#def quiver(file, time, depth):
    #code here

#def heatmap(file, time, depth):
    # code here

#def contourf(file, time, depth):
    # code here