import streamlit as st
import netCDF4 as nc
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from io import BytesIO

def datasetmanagement_page():
    st.title("Dataset Management")

    # File uploader for multiple .nc files in the sidebar
    files_upload = st.file_uploader("Upload datasets", type=["nc"], accept_multiple_files=True)

    # Initialize a mapping of datetime strings to their corresponding file names
    datetime_to_file_map = defaultdict(list)

    depth_levels = None  # Variable to store the number of depth levels

    if files_upload:
        all_datetime_strings = []
        variables_not_dimensions = []

        for uploaded_file in files_upload:
            nc_file = nc.Dataset('in-memory', memory=uploaded_file.getvalue(), diskless=True)

            # Extract depth information from the first file
            if 'depth' in nc_file.dimensions and depth_levels is None:
                depth_dim = nc_file.dimensions['depth']
                depth_levels = len(depth_dim)  # Store the number of depth levels

            time_var = nc_file.variables['time']
            time_units = time_var.units
            datetimes = nc.num2date(time_var[:], units=time_units)

            for dt in datetimes:
                dt_str = str(dt)
                all_datetime_strings.append(dt_str)
                datetime_to_file_map[dt_str].append(uploaded_file.name)

            # Identify variables that are not dimensions
            if not variables_not_dimensions:  # If not already determined
                for var_name, variable in nc_file.variables.items():
                    if var_name not in nc_file.dimensions:
                        variables_not_dimensions.append(var_name)

            nc_file.close()

        # Display time select box
        if all_datetime_strings:
            selected_datetime_str = st.sidebar.selectbox(
                "Time:",
                options=all_datetime_strings,
                index=0  # Default to the first option
            )

            #associated_files = datetime_to_file_map[selected_datetime_str]
            #st.write(f"Selected datetime: {selected_datetime_str}")
            #for file in associated_files:
                #st.write(f"From file: {file}")
        else:
            st.sidebar.write("No datetime values found.")

        # Display depth slider if depth information is available
        if depth_levels is not None:
            selected_depth = st.sidebar.slider("Depth", 0, depth_levels - 1, value=0)
            #st.write(f"Selected depth level: {selected_depth}")
        else:
            st.sidebar.write("No depth information available.")

        # If time and depth exists...
        if all_datetime_strings:
            if depth_levels is not None:
                selected_visualization = st.sidebar.selectbox(
                    "Visualization Option:",
                    options=["None", "Heat Map", "something else"],
                    index=0  # Default to the first option
                )
                if selected_visualization == "Heat Map":
                    if variables_not_dimensions:
                        selected_variable = st.sidebar.selectbox(
                            "Choose a variable for analysis:",
                            options=["None"] + variables_not_dimensions
                        )
                        # At the point where you decide to call heatmap() if selected_variable is not "None":
                        # Assuming 'uploaded_file' is a BytesIO object from 'files_upload'
                        # Instead of passing 'filename', pass the BytesIO object or its content

                        if selected_variable != "None":
                            associated_files = datetime_to_file_map[selected_datetime_str]
                            if associated_files:
                                # filename variable here would be misleading, it's actually the file content
                                file_content = next(
                                    (file.getvalue() for file in files_upload if file.name == associated_files[0]),
                                    None)

                                if file_content:
                                    # Call the heatmap function with the file content
                                    heatmap(file_content, selected_datetime_str, selected_depth, selected_variable)



                    else:
                        st.sidebar.write("No variable information available.")


def parse_datetime(datetime_str):
    # List of potential datetime formats
    datetime_formats = [
        "%Y-%m-%d %H:%M:%S.%f",  # Format with full precision
        "%Y-%m-%d %H:%M:%S",  # Format without microseconds
        "%Y-%m-%d %H:%M",  # Format without seconds
        "%Y-%m-%d %H",  # Format without minutes and seconds
        "%Y-%m-%d",  # Date only, no time
        # Add more formats as needed
    ]

    # Try parsing the datetime string with each format
    for fmt in datetime_formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue  # Try the next format

    # Handle the case where none of the formats matched
    raise ValueError(f"Date format for '{datetime_str}' is not supported.")


def heatmap(file_content, datetime_str, depth, variable):
    # Load the NetCDF file from BytesIO object
    nc_file = nc.Dataset('in-memory', memory=file_content)

    try:
        # Convert the selected datetime string back to a datetime object
        selected_datetime = parse_datetime(datetime_str)

        # Find the index of the selected time
        time_var = nc_file.variables['time']
        time_units = time_var.units
        selected_time_index = np.where(nc.num2date(time_var[:], units=time_units) == selected_datetime)[0][0]

        # Access the data for the selected variable
        data = nc_file.variables[variable]

        # Assuming the data structure is [time, depth, lat, lon]
        selected_data = data[selected_time_index, depth, :, :]

        # Get latitude and longitude values for plotting
        lat = nc_file.variables['lat'][:]
        lon = nc_file.variables['lon'][:]

        # Create the heatmap with a smaller figure size
        # Adjust the figsize (width, height) as needed to fit your Streamlit layout
        fig, ax = plt.subplots()  # Example: Smaller figure size
        c = ax.pcolormesh(lon, lat, selected_data, cmap='coolwarm')
        #ax.set_title(f'{variable} at depth {depth} on {datetime_str}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        fig.colorbar(c, ax=ax, label=variable)

        fig.tight_layout(pad=1.0)

        buf = BytesIO()
        fig.savefig(buf, format="png", transparent=True)
        st.image(buf, width=1080)

        # Display the plot
        #st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating heatmap: {e}")
    finally:
        nc_file.close()

