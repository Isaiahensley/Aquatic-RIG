import streamlit as st


def about_page():
    howtouse()
    st.write("---")
    netcdf4()
    st.write("---")
    usecase()


# ----------------------------------------------NetCDF4---------------------------------------------------
def netcdf4():
        st.title("What is NetCDF4 (.nc)")

        st.write("""
        NetCDF (Network Common Data Form) files are a type of file format used to store multidimensional scientific data, particularly in fields such as atmospheric and oceanographic research, climate modeling, and geoscience. Here's a concise yet comprehensive description:
    
        "NetCDF is a self-describing, machine-independent binary file format for storing scientific data, primarily gridded data. It supports the creation, access, and sharing of array-oriented scientific data, allowing researchers to store large datasets efficiently and effectively. NetCDF files can contain multiple dimensions, variables, and attributes, providing a flexible and scalable solution for organizing complex data structures. The format is widely used in fields such as atmospheric science, oceanography, climate modeling, and geoscience due to its ability to handle multidimensional datasets and maintain metadata integrity. NetCDF files are supported by a variety of programming languages and data analysis tools, making them a standard choice for scientific data storage and exchange."
        """, unsafe_allow_html=True, text_align='left')

        st.write("For more information, you can visit the [NetCDF Overview page](https://docs.unidata.ucar.edu/netcdf-c/current/) on Unidata's website.", unsafe_allow_html=True, text_align='left')
        st.image("images/ocean.jpg", caption="Image taken from: https://oceanexplorer.noaa.gov/world-oceans-day-2015/how-much-of-the-seafloor-is-left-to-explore.html")


# ----------------------------------------------HOW TO USE-------------------------------------------------
def howtouse():
        st.title("How To Use")

        # Getting Started
        with st.expander("Getting Started", expanded=False):
            st.write("To get started you'll need to either upload an aquatic dataset or use our preset example dataset")
            with st.container(border=True):
                st.image('how-to-use/initial.PNG')

        # Uploading Files
        with st.expander("Uploading Files", expanded=False):
            st.write("If you choose to upload your own aquatic dataset each file must meet the following requirements:")
            st.write("Each file must not exceed 200MB  \n")
            st.write("Each file must have a dimension for Time, Depth, Latitude, and Longitude.  \n")
            st.write("Multiple Files can be uploaded if they are similar but have data for different Time dimensions  \n")
            st.write("All files must have the same names for each dimension and variable  \n")
            with st.container(border=True):
                st.image('how-to-use/uploading.PNG')

        # Example Dataset
        with st.expander("Example Dataset", expanded=False):
            st.write(
                "If you choose to use our preset Example Dataset, we have included 5 NetCDF4 files. "
                "This dataset includes data collected at the Southern California Bight, "
                "a coastal region in the southwestern United States."
            )
            st.write(
                "Each file represents data collected every 3 hours, starting on October 28, 2022, at 3pm."
            )
            st.write(
                "These files have data collected over 14 depth levels in meters. "
                "Each of these levels is represented as follows:  \n"
                
                "0, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500, and 1000.\n"
            )
            st.write(
                "The variables measured at each of these dimensions are:  \n"
                
                "**temp** - Temperature in Celsius (°C).  \n"
                
                "**salt** - Salinity levels.  \n"
                
                "**u** - Movement in the horizontal direction, representing the east-west component of the water current. "
                "This helps determine the direction and velocity as currents move horizontally.  \n"
                
                "**v** - Movement in the vertical direction, representing the north-south component of the water current. "
                "This helps determine the direction and velocity as currents move vertically.  \n"
                
                "**zeta** - Sea Surface level.  \n"
            )
            st.write(
                "For more information, visit:  \n"
                
                "[SCCOOS ROMS Model Output](https://sccoos.org/roms-model-output/)  \n"
                
                "[ERDDAP SCCOOS](https://erddap.sccoos.org/erddap/files/roms_fcst/)"
            )
            with st.container(border=True):
                st.image('how-to-use/example.PNG')

        # Uploaded File Dimensions
        with st.expander("Uploaded File Dimensions", expanded=False):
            st.write("After uploading files you will need to select which of the dimension names in your dataset represent "
                     "Time, Depth, Latitude, and Longitude.")

            st.write("**If using our example dataset, we have already predefined these dimension names "
                     "and this page will be skipped**")

            with st.container(border=True):
                st.image('how-to-use/dimensions.PNG')

            st.write("In this example, the dimension names found in the dataset are time, depth, lat, and lon. We will put these in their respective dimensions.  \n"
                     "**time** = Time  \n"
                     "**depth** = Depth  \n"
                     "**lat** = Latitude  \n"
                     "**lon** = Longitude")
            with st.container(border=True):
                st.image('how-to-use/dimensions2.PNG')

        # Visualization Options
        with st.expander("Visualization Options", expanded=False):
            st.write("After selecting the example dataset or uploading files, you will need to select a visualization "
                     "option to view your dataset.")

            st.write("Currently, we offer two visualization options: Heat Map and Quiver Plot.")
            with st.container(border=True):
                st.image('how-to-use/visoption.PNG')

            st.write("**Heat Map**  \n"
            "This tool is designed for visualizing a chosen variable by coloring each data point according to its value. "
            "Higher values are illustrated with warm colors like red, while lower values are shown in cooler colors "
            "like blue.  \n")

            st.write("**Quiver Plot**  \n"
            "This tool is designed for visualizing vector fields like ocean currents. Each arrows size and direction "
            "visualizes the flow's direction and velocity. This visualization requires the horizontal (u) and vertical (v) "
            "vectors.  \n")

            with st.container(border=True):
                st.image('how-to-use/visoption2.PNG')

        # Heat Map Variable
        with st.expander("Heat Map Variable", expanded=False):
            st.write("After selecting Heat Map as your visualization option, you will need to select the variable you "
                     "would like to represent.")

            st.write("The values for the variable you select will be shown on the Heat Map for every Latitude and Longitude "
                     "coordinate. You can also change the Time and Depth to see how this influences the data values.")

            with st.container(border=True):
                st.image('how-to-use/heatvar.PNG')

            st.write("In this example, the variable options we have are temp, salt, u, v, and zeta. With this dataset, "
                     "if you choose temp, you will get a Heat Map displaying all the temperature values at each location.")

            with st.container(border=True):
                st.image('how-to-use/heatvar2.PNG')

        # Heat Map
        with st.expander("Heat Map", expanded=False):
            st.write("After selecting a variable for the Heat Map, you will see a visulization on the right that depicts "
                     "the variable you selected at each latitude and longitude coordinate.")

            st.write("Each location's color ranges in a gradient from red to blue, with higher values appearing more red, "
                     "and lower values, more blue.")

            st.write("On the left you are given options to change the time and depth. When these values are changed, "
                     "the visual on the right will update.")

            st.write("**Currently each visuals gradient range is based on the current depth and time. This means that "
                     "as you change these dimensions the color gradient may represent different values.**")
            with st.container(border=True):
                st.image('how-to-use/heat.PNG')

        # Quiver Plot Variables
        with st.expander("Quiver Plot Variables", expanded=False):
            st.write("After selecting Quiver Plot as your visualization option, you will need to select the Horizontal (u) "
                     "and Vertical (v) variables.")

            st.write("These two variables represent vectors so that the water currents can be displayed in respect to "
                     "the currents velocity and direction.")
            with st.container(border=True):
                st.image('how-to-use/quivervar.PNG')

            st.write("**Horizontal (u)**  \n"
                     "Typically referenced as 'u' in a dataset, it is a variable that captures the movement in the "
                     "horizontal direction, representing the east-west component of the current. "
                     "It helps determine the direction and velocity as water currents move horizontally.")

            st.write("**Vertical (v)**  \n"
                     "Typically referenced as 'v' in a dataset, it is a variable that captures the movement in the "
                     "vertical direction, representing the north-south component of the current. "
                     "It helps determine the direction and velocity as water currents move vertically.")

            with st.container(border=True):
                st.image('how-to-use/quivervar2.PNG')

        # Quiver Plot
        with st.expander("Quiver Plot", expanded=False):
            st.write("After selecting both variables for the Quiver Plot, you will see a visulization on the right that "
                     "depicts the u and v at each latitude and longitude coordinate.")

            st.write("Each arrows size and direction visualizes the flow's direction and velocity.")

            st.write("On the left you are given options to change the time and depth. When these values are changed, "
                     "the visual on the right will update.")

            with st.container(border=True):
                st.image('how-to-use/quiver.PNG')


# ----------------------------------------------Use Cases-------------------------------------------------
def usecase():
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