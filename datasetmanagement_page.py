import streamlit as st
import netCDF4 as nc
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from io import BytesIO


def dataset_management_page():
    # File uploader for multiple .nc files
    files_upload = file_uploader()

    # Extract data from uploaded files
    if files_upload is not None:
        all_datetime_strings, depth_levels, variables_not_dimensions, datetime_to_file_map = extract_file_data(
            files_upload)

        # Checks if all data exists for visualization
        if data_check(files_upload, all_datetime_strings, depth_levels, variables_not_dimensions,
                      datetime_to_file_map):
            # Creates Visualization Option selectbox and returns user selection
            selected_visualization = visualization_selectbox()

            # --------------HEAT MAP VISUALIZATION-----------
            # If selection is "Heat Map"...
            if selected_visualization == "Heat Map":
                selected_variable = variable_selectbox(variables_not_dimensions)
                if selected_variable != "None":
                    # Create Time selectbox
                    selected_datetime_str, associated_files = time_selectbox(datetime_to_file_map, all_datetime_strings)

                    # Create Depth slider
                    selected_depth = depth_slider(depth_levels)

                    associated_files = datetime_to_file_map[selected_datetime_str]
                    if associated_files:
                        # filename variable here would be misleading, it's actually the file content
                        file_content = next(
                            (file.getvalue() for file in files_upload if file.name == associated_files[0]),
                            None)

                        if file_content:
                            # Call the heatmap function with the file content
                            heatmap(variables_not_dimensions, file_content, selected_datetime_str, selected_depth,
                                    selected_variable)

            # --------------QUIVER PLOT VISUALIZATION-----------
            # If selection is "Quiver Plot"...
            elif selected_visualization == "Quiver Plot":
                selected_xvelocity = xvelocity_selectbox(variables_not_dimensions)
                selected_yvelocity = yvelocity_selectbox(variables_not_dimensions)
                # If both selections aren't "None"
                if selected_xvelocity != "None" and selected_yvelocity != "None":
                    # If both selections aren't the same variable.
                    if selected_xvelocity != selected_yvelocity:
                        # Create Time selectbox
                        selected_datetime_str, associated_files = time_selectbox(datetime_to_file_map,
                                                                                 all_datetime_strings)

                        # Create Depth slider
                        selected_depth = depth_slider(depth_levels)

                        associated_files = datetime_to_file_map[selected_datetime_str]
                        if associated_files:
                            # filename variable here would be misleading, it's actually the file content
                            file_content = next(
                                (file.getvalue() for file in files_upload if file.name == associated_files[0]),
                                None)

                            if file_content:
                                # Call the heatmap function with the file content
                                quiverplot(variables_not_dimensions, file_content, selected_datetime_str,
                                           selected_depth, selected_xvelocity, selected_yvelocity)
def file_uploader():
    files_upload = st.file_uploader("Upload datasets", type=["nc"], accept_multiple_files=True)
    return files_upload


def extract_file_data(files_upload):
    # Initialize defaults
    datetime_to_file_map = defaultdict(list)
    all_datetime_strings = []
    variables_not_dimensions = []
    depth_levels = None

    # Extracts info from the uploaded nc files
    if files_upload:
        all_datetime_strings = []
        variables_not_dimensions = []

        for uploaded_file in files_upload:
            nc_file = nc.Dataset('in-memory', memory=uploaded_file.getvalue(), diskless=True)

            # Extract depth information from the first file
            if 'depth' in nc_file.dimensions:
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
    return all_datetime_strings, depth_levels, variables_not_dimensions, datetime_to_file_map


def data_check(files_upload, all_datetime_strings, depth_levels, variables_not_dimensions, datetime_to_file_map):
    check = True
    # Check if files have been uploaded
    if not files_upload:
        # No files have been uploaded yet, so there's nothing to check
        return False

    if all_datetime_strings is None:
        check = False
        st.text("Could not convert date dimensions to datetime")
    if depth_levels is None:
        check = False
        st.text("Could not get depth levels")
    if variables_not_dimensions is None:
        check = False
        st.text("Could not find variables that are not dimensions")
    if datetime_to_file_map is None:
        check = False
        st.text("Could not map date to respective file")
    return check


def visualization_selectbox():
    selected_visualization = st.sidebar.selectbox(
        "Visualization Option:",
        options=["None", "Heat Map", "Quiver Plot"],
        index=0  # Default to the first option
    )
    return selected_visualization


def variable_selectbox(variables_not_dimensions):
    selected_variable = st.sidebar.selectbox(
        "Choose a variable for analysis:",
        options=["None"] + variables_not_dimensions
    )
    return selected_variable

def xvelocity_selectbox(variables_not_dimensions):
    selected_xvelocity = st.sidebar.selectbox(
        "Choose the velocity in the X direction:",
        options=["None"] + variables_not_dimensions
    )
    return selected_xvelocity

def yvelocity_selectbox(variables_not_dimensions):
    selected_yvelocity = st.sidebar.selectbox(
        "Choose the velocity in the Y direction:",
        options=["None"] + variables_not_dimensions
    )
    return selected_yvelocity

def time_selectbox(datetime_to_file_map, all_datetime_strings):
    # Display time select box
    if all_datetime_strings:
        selected_datetime_str = st.sidebar.selectbox(
            "Time:",
            options=all_datetime_strings,
            index=0  # Default to the first option
        )
        associated_files = datetime_to_file_map[selected_datetime_str]
    else:
        st.sidebar.write("No datetime values found.")
    return selected_datetime_str, associated_files


def depth_slider(depth_levels):
    # Display depth slider
    if depth_levels is not None:
        selected_depth = st.sidebar.slider("Depth", 0, depth_levels - 1, value=0)
        # st.write(f"Selected depth level: {selected_depth}")
    else:
        st.sidebar.write("No depth information available.")
    return selected_depth


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


def heatmap(variables_not_dimensions, file_content, datetime_str, depth, variable):
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

        # Create the heatmap
        fig, ax = plt.subplots()
        c = ax.pcolormesh(lon, lat, selected_data, cmap='coolwarm')

        # Adjust color
        color = "lightblue"

        # Set axis labels with specified color
        ax.set_xlabel('Longitude', color=color)
        ax.set_ylabel('Latitude', color=color)

        # Set tick labels and ticks color
        ax.tick_params(colors=color, which='both')  # 'both' applies changes to both major and minor ticks

        # Set spine colors
        for spine in ax.spines.values():
            spine.set_color(color)

        # Create colorbar with specified label color
        colorbar = fig.colorbar(c, ax=ax, label=variable)
        colorbar.set_label(variable, color=color)

        # Set colorbar tick color and tick labels to specified color
        colorbar.ax.yaxis.set_tick_params(color=color)  # This sets the tick color
        plt.setp(plt.getp(colorbar.ax.axes, 'yticklabels'), color=color)  # This sets the tick label color

        fig.tight_layout(pad=1.0)

        # Enhance the picture quality by increasing the DPI (this may lead to longer load times)
        dpi = 500  # Adjust DPI to your needs for higher resolution

        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, transparent=True)
        st.image(buf, width=1080)

    except Exception as e:
        st.error(f"Error generating heatmap: {e}")
    finally:
        nc_file.close()


def quiverplot(variables_not_dimensions, file_content, datetime_str, depth, selected_xvelocity, selected_yvelocity):
    # Load the NetCDF file from BytesIO object
    nc_file = nc.Dataset('in-memory', memory=file_content)

    try:
        # Convert the selected datetime string back to a datetime object
        selected_datetime = parse_datetime(datetime_str)

        # Find the index of the selected time
        time_var = nc_file.variables['time']
        time_units = time_var.units
        selected_time_index = np.where(nc.num2date(time_var[:], units=time_units) == selected_datetime)[0][0]

        # Access the data for the selected u and v velocity variables
        u_data = nc_file.variables[selected_xvelocity][selected_time_index, depth, :, :]
        v_data = nc_file.variables[selected_yvelocity][selected_time_index, depth, :, :]

        # Ensure lat and lon are 2D arrays for quiver plotting
        lat = nc_file.variables['lat'][:]
        lon = nc_file.variables['lon'][:]
        Lon, Lat = np.meshgrid(lon, lat)

        # Optionally, reduce the density of arrows for clarity
        skip = (slice(None, None, 5), slice(None, None, 5))  # Adjust the slicing for desired arrow density
        u_data = u_data[skip]
        v_data = v_data[skip]
        Lon = Lon[skip]
        Lat = Lat[skip]

        # Setting up the plot with a dark background for white elements to stand out
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))
        q = ax.quiver(Lon, Lat, u_data, v_data, color='white')  # Set arrow color to white

        # Include a key to indicate scale, with text in white
        ax.quiverkey(q, X=0.9, Y=1.05, U=10, label='10 units', labelpos='E', color='white')

        # Set axis labels and title with white text
        ax.set_xlabel('Longitude', color='white')
        ax.set_ylabel('Latitude', color='white')
        #ax.set_title(f'Quiver plot for {selected_xvelocity} and {selected_yvelocity} at depth {depth} on {datetime_str}', color='white')

        # Changing tick parameters to white
        ax.tick_params(axis='both', colors='white')

        fig.tight_layout()

        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300, transparent=True)
        #st.image(buf, use_column_width=True)
        st.image(buf, width=1080)
    except Exception as e:
        st.error(f"Error generating quiver plot: {e}")
    finally:
        nc_file.close()


