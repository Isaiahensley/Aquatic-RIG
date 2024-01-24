import streamlit as st
from PIL import Image


def home_page():

    st.sidebar.markdown("Dataset-Related Links")
    st.sidebar.button("Testing")

    st.sidebar.markdown("Software-Related Links")
    st.sidebar.button("Testing2")


    left_col, right_col = st.columns(2)
    with left_col:
        image = Image.open('AquaRigLogo.png')
        st.image(image, width=400, output_format="PNG")

    right_col.markdown("# Aquatic Rig")
    right_col.markdown("### a web application for analyzing time series water data")
    right_col.markdown("")
    right_col.markdown("")
    right_col.markdown("Created by Isaiah Hensley, Maria Black, Sudeep Paudel, Richard Peters")
    right_col.markdown("Louisiana State University Shreveport")


    st.divider()
    st.write("Test")