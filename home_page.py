import streamlit as st
from PIL import Image


def home_page():

    st.sidebar.markdown("Dataset-Related Links")
    st.sidebar.link_button("GitHub Page", "https://github.com/Isaiahensley/Aquatic-RIG")

    st.sidebar.markdown("Software-Related Links")
    st.sidebar.link_button("Matplotlib", "https://matplotlib.org/")
    st.sidebar.link_button("Streamlit", "https://streamlit.io/")
    st.sidebar.link_button("NumPy", "https://numpy.org/")


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