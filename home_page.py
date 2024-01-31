import streamlit as st


def home_page():
    st.title("Aquatic Rig Home Page")

    left_col, right_col = st.columns(2)

    right_col.markdown("# Aquatic Rig")
    right_col.markdown("### A tool for ...")
    right_col.markdown("**Created by Isaiah Hensley, Maria Black, Sudeep Paudel, Richard Peters**")
    right_col.markdown("**Louisiana State University Shreveport**")