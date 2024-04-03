import streamlit as st


# The About Page Structure
def about_page():
    # Title
    st.title("Data Visualization Platform")

    st.markdown(
        """
        Welcome to our data visualization platform! We help you turn your data into actionable insights.
        """
    )

    st.write("---")

    st.header("Key Features")

    st.write(
        """
        Here are some of the features that make our platform stand out:
        - Interactive Visualizations
        - Customizable Dashboards
        - Real-time Data Updates
        - Seamless Integration with Various Data Sources
        """
    )

    st.write("---")

    st.header("Case Studies")

    st.write(
        """
        Check out some of our success stories:
        - Lorem Ipsum Case Study 1
          ![Case Study 1](https://via.placeholder.com/400x200)
        - Lorem Ipsum Case Study 2
          ![Case Study 2](https://via.placeholder.com/400x200)
        """
    )

    st.write("---")

    st.header("Testimonials")

    st.write(
        """
        Here's what our users are saying:
        - "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut aliquam mauris ac tortor condimentum, nec viverra nisl aliquet." - John Doe
        - "Nullam eu metus nec justo aliquet pharetra. Mauris non nisi ac risus commodo finibus ut nec ex." - Jane Smith
        """
    )

    st.write("---")

    st.header("Get Started")

    st.write(
        """
        Ready to experience the power of data visualization? Sign up for a free trial today!
        """
    )

    st.title("About NetCDF Files")

    st.write("""
    NetCDF (Network Common Data Form) files are a type of file format used to store multidimensional scientific data, particularly in fields such as atmospheric and oceanographic research, climate modeling, and geoscience. Here's a concise yet comprehensive description:

    "NetCDF is a self-describing, machine-independent binary file format for storing scientific data, primarily gridded data. It supports the creation, access, and sharing of array-oriented scientific data, allowing researchers to store large datasets efficiently and effectively. NetCDF files can contain multiple dimensions, variables, and attributes, providing a flexible and scalable solution for organizing complex data structures. The format is widely used in fields such as atmospheric science, oceanography, climate modeling, and geoscience due to its ability to handle multidimensional datasets and maintain metadata integrity. NetCDF files are supported by a variety of programming languages and data analysis tools, making them a standard choice for scientific data storage and exchange."
    """, unsafe_allow_html=True, text_align='left')

    st.write("For more information, you can visit the [NetCDF Overview page](https://docs.unidata.ucar.edu/netcdf-c/current/) on Unidata's website.", unsafe_allow_html=True, text_align='left')
    st.image("images/ocean.jpg", caption="Image taken from: https://oceanexplorer.noaa.gov/world-oceans-day-2015/how-much-of-the-seafloor-is-left-to-explore.html")


# The Main Function
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
