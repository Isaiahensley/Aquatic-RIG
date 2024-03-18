import streamlit as st

def about_page():
    st.title("About NetCDF Files")
    st.write("""
    NetCDF (Network Common Data Form) files are a type of file format used to store multidimensional scientific data, particularly in fields such as atmospheric and oceanographic research, climate modeling, and geoscience. Here's a concise yet comprehensive description:

    "NetCDF is a self-describing, machine-independent binary file format for storing scientific data, primarily gridded data. It supports the creation, access, and sharing of array-oriented scientific data, allowing researchers to store large datasets efficiently and effectively. NetCDF files can contain multiple dimensions, variables, and attributes, providing a flexible and scalable solution for organizing complex data structures. The format is widely used in fields such as atmospheric science, oceanography, climate modeling, and geoscience due to its ability to handle multidimensional datasets and maintain metadata integrity. NetCDF files are supported by a variety of programming languages and data analysis tools, making them a standard choice for scientific data storage and exchange."
    """)

def main():
    st.sidebar.title("Navigation")
    pages = {
        "About": about_page
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
