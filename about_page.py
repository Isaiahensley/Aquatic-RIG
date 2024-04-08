import streamlit as st


def about_page():
    st.title("Data Visualization Platform")

    st.markdown(
        """
        Welcome to our data visualization platform! We help you turn your data into actionable insights.
        """
    )

    st.header("Use Cases")

    st.write(
        """  NetCDF data are self describing meaning these files includes information about
        the data it contains such as when data elements are captured and what units of measurement were used. 
        They contains wide range of information including ocean temperature, salinity, current velocities, sealevel etc.
        \n 
        Here are some of the use cases for visualizing NetCDF aquatic dataset: 
        
        - Oceanographic Research: Researchers can use NetCDF visuals to showcase ocean temperature, 
                                   current salinity over time and space. It is useful for 
                                   studying ocean circulation pattern, track movement of water masses.

        - Climate change Monitoring: 
                                    NetCDF data can show the effect of climate change on aquatic ecosystem
        - Education Tools
                                    Visuals obtained from NetCDF can be used as education tool to learn about 
                                    oceanography, climate science and environmental issue
        - Fisheries Management
        - Coastal Zone Management
        """
    )
    st.title("About NetCDF Files")

    st.write("""NetCDF (Network Common Data Form) files are a type of file format used to store multidimensional 
    scientific data, particularly in fields such as atmospheric and oceanographic research, climate modeling, 
    and geoscience. Here's a concise yet comprehensive description:

    "NetCDF is a self-describing, machine-independent binary file format for storing scientific data, primarily 
    gridded data. It supports the creation, access, and sharing of array-oriented scientific data, 
    allowing researchers to store large datasets efficiently and effectively. NetCDF files can contain multiple 
    dimensions, variables, and attributes, providing a flexible and scalable solution for organizing complex data 
    structures. The format is widely used in fields such as atmospheric science, oceanography, climate modeling, 
    and geoscience due to its ability to handle multidimensional datasets and maintain metadata integrity. NetCDF 
    files are supported by a variety of programming languages and data analysis tools, making them a standard choice 
    for scientific data storage and exchange." , unsafe_allow_html=True, text_align='left"
    """)

    st.write(
        "For more information, you can visit the [NetCDF Overview page](https://docs.unidata.ucar.edu/netcdf-c/current/) on Unidata's website.",
        unsafe_allow_html=True, text_align='left')
    st.image("images/ocean.jpg",
             caption="Image taken from: https://oceanexplorer.noaa.gov/world-oceans-day-2015/how-much-of-the-seafloor-is-left-to-explore.html")


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

