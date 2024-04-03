import os
import streamlit as st
import netCDF4 as nc
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from io import BytesIO


# Initialize session_state variables safely
def initialize_state():
    if 'current_step' not in st.session_state:
        st.session_state['current_step'] = 0
    if 'files_upload' not in st.session_state:
        st.session_state['files_upload'] = None


# Define steps for the workflow
def increment_step():
    st.session_state['current_step'] += 1


def decrement_step():
    if st.session_state['current_step'] > 0:
        st.session_state['current_step'] -= 1


def load_example_dataset():
    example_files = []
    example_dataset_folder = 'example_dataset'
    for filename in os.listdir(example_dataset_folder):
        if filename.endswith('.nc'):
            file_path = os.path.join(example_dataset_folder, filename)
            with open(file_path, 'rb') as f:
                bytes_io = BytesIO(f.read())
                bytes_io.name = filename  # Set the name attribute to the filename
                example_files.append(bytes_io)
    return example_files


# Main function to manage the dataset page
def dataset_management_page():
    initialize_state()

    # ------------------------
    # Step 0: File Upload Page
    # ------------------------

    if st.session_state['current_step'] == 0:
        st.session_state['files_upload'] = file_uploader()
        st.write("")
        st.session_state['example_dataset'] = st.checkbox("Use Example Dataset")
        st.write("")
        next_button(st.session_state['files_upload'] or st.session_state['example_dataset'])
        # Proceed after next button is pressed if files are uploaded or example dataset is checked

    # -----------------------------------
    # Step 1: Dimension Selection Page (Skip if using example dataset)
    # -----------------------------------

    if st.session_state['current_step'] == 1:

        # Decide which files to use: uploaded files or example dataset files
        # If both files are uploaded and the example dataset is checked it will ignore the uploaded files
        files_to_process = None
        if st.session_state['example_dataset']:
            # Load example dataset files
            files_to_process = load_example_dataset()

            # Save dimension names we know are used in the example dataset to session state
            st.session_state['time'] = "time"
            st.session_state['depth'] = "depth"
            st.session_state['lat'] = "lat"
            st.session_state['lon'] = "lon"

            # Skip Dimension Selection Page since example dataset was selected, and we already know the dimensions
            increment_step()

        elif st.session_state['files_upload']:
            # Use the files uploaded by the user
            files_to_process = st.session_state['files_upload']

            # Get all dimensions in the uploaded .nc files
            dimensions = extract_dimensions(files_to_process)

            time_option = st.selectbox(
                "Time",
                dimensions,
                index=None,
                placeholder="Select Time Dimension",
            )

            depth_option = st.selectbox(
                "Depth",
                dimensions,
                index=None,
                placeholder="Select Depth Dimension",
            )

            lat_option = st.selectbox(
                "Latitude",
                dimensions,
                index=None,
                placeholder="Select Latitude Dimension",
            )

            lon_option = st.selectbox(
                "Longitude",
                dimensions,
                index=None,
                placeholder="Select Longitude Dimension",
            )

            # Check if none of the selections are None
            if None not in (time_option, depth_option, lat_option, lon_option):
                # Check if all selections are unique
                if len({time_option, depth_option, lat_option, lon_option}) == 4:
                    # If both conditions are met save the selections made to each dimension for later use
                    st.session_state['time'] = time_option
                    st.session_state['depth'] = depth_option
                    st.session_state['lat'] = lat_option
                    st.session_state['lon'] = lon_option

            # Create columns that let the next and back buttons display side by side.
            left, right, filler = st.columns([1, 1, 15])

            # Put Next button on the right (after condition is met)
            # This will take you to the Visualization Selection Page
            with right:
                next_button(None not in (time_option, depth_option, lat_option, lon_option) and
                            len({time_option, depth_option, lat_option, lon_option}) == 4)

            # Put Back button on the left
            # This will take you to the File Upload Page
            with left:
                back_button()

        # Save files_to_process to session state (either uploaded files or example dataset)
        st.session_state['files_to_process'] = files_to_process

    # -----------------------------------
    # Step 2: Visualization Selection Page
    # -----------------------------------

    if st.session_state['current_step'] == 2:


        # Extract data from either uploaded or example dataset files
        if st.session_state['files_to_process']:
            (st.session_state['all_datetime_strings'],
             st.session_state['depth_levels'],
             st.session_state['variables_not_dimensions'],
             st.session_state['datetime_to_file_map']) = extract_file_data(st.session_state['files_to_process'])

        # Visualization Selection box
        selected_visualization = visualization_selectbox()

        # Create columns that let the next and back buttons display side by side.
        left, right, filler = st.columns([1, 1, 15])

        # If a visualization option is chosen...
        if selected_visualization is not None:
            st.session_state['selected_visualization'] = selected_visualization

        # Put Next button on the right (after condition is met)
        # This will take you to the Variable Selection Page
        with right:
            next_button(selected_visualization is not None)

        # Put Back button on the left
        # This will take you to the File Upload Page
        with left:
            back_button()

    # -------------------------------
    # Step 3: Variable Selection Page
    # -------------------------------

    if st.session_state.current_step == 3 and 'selected_visualization' in st.session_state:

        # If Heat Map is selected...
        if st.session_state.selected_visualization == "Heat Map":

            # Ask user to select variable for heat map
            selected_variable = variable_selectbox(st.session_state['variables_not_dimensions'])

            # Create columns that let the next and back buttons display side by side.
            left, right, filler = st.columns([1, 1, 15])

            # If a variable has been selected...
            if selected_variable is not None:
                st.session_state.selected_variable = selected_variable

            # Put Next button on the right (after variable is selected)
            # This will take you to the Visualize Page (Heat Map)
            with right:
                next_button(selected_variable is not None)

        elif st.session_state.selected_visualization == "Quiver Plot":
            selected_xvelocity = xvelocity_selectbox(st.session_state['variables_not_dimensions'])
            selected_yvelocity = yvelocity_selectbox(st.session_state['variables_not_dimensions'])

            # Create columns that let the next and back buttons display side by side.
            left, right, filler = st.columns([1, 1, 15])

            if selected_xvelocity is not None and selected_yvelocity is not None and selected_xvelocity != selected_yvelocity:
                st.session_state.selected_xvelocity = selected_xvelocity
                st.session_state.selected_yvelocity = selected_yvelocity

            # Put Next button on the right (after variable is selected)
            # This will take you to the Visualize page (Quiver Plot)
            with right:
                next_button(selected_xvelocity is not None and selected_yvelocity is not None and selected_xvelocity != selected_yvelocity)

        # Put Back button on the left
        # This will take you to the Visualization Selection Page
        with left:
            back_button()

    # --------------------------
    # Step 4: Visualize Page
    # --------------------------

    if st.session_state.current_step == 4:
        # columns for have left 1/3 of the screen and right 2/3 of the screen
        # left will be used for slider and buttons while right will have the matplotlib visual
        left_column, right_column = st.columns([1, 3])

        # Left column filled with depth slider and time selectbox as well as a back button at the bottom
        with left_column:
            selected_datetime_str, associated_files = time_selectbox(st.session_state['datetime_to_file_map'],
                                                                     st.session_state['all_datetime_strings'])
            selected_depth = depth_slider(st.session_state['depth_levels'])

            # I used this markdown to fill up empty space so the back button would be on the bottom
            st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>",
                        unsafe_allow_html=True)
            back_button()

        # Gets the files and makes sure they exist
        current_files = st.session_state['files_to_process']

        # Goes through all the files and makes sure they are read as bits to be passed into the MatPlotLib visuals
        if associated_files and current_files:
            file_content = next((file for file in current_files if file.name == associated_files[0]), None)

            if file_content is not None:
                # Read the content of the file into bytes
                file_content.seek(0)
                file_bytes = file_content.read()

                # If Heat Map is selected and a variable is chosen, create a heatmap with that variable
                if st.session_state.selected_visualization == "Heat Map" and 'selected_variable' in st.session_state:
                    with right_column:
                        heatmap(st.session_state['variables_not_dimensions'], file_bytes, selected_datetime_str,
                                selected_depth, st.session_state.selected_variable)

                # If Quiver Plot is selected and a U and V variable is chosen, create a Quiver Plot with them
                elif st.session_state.selected_visualization == "Quiver Plot" and 'selected_xvelocity' in st.session_state and 'selected_yvelocity' in st.session_state:
                    with right_column:
                        quiverplot(st.session_state['variables_not_dimensions'], file_bytes, selected_datetime_str,
                                   selected_depth, st.session_state.selected_xvelocity,
                                   st.session_state.selected_yvelocity)
            else:
                st.write("No file content available")


# File uploader widget that accepts multiple .nc files
def file_uploader():
    files_upload = st.file_uploader("Upload datasets", type=["nc"], accept_multiple_files=True)
    return files_upload


# Extract neccessary data from the files that are uploaded or the ones store in the example dataset
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
            if st.session_state['depth'] in nc_file.dimensions:
                depth_dim = nc_file.dimensions[st.session_state['depth']]
                depth_levels = len(depth_dim)  # Store the number of depth levels

            time_var = nc_file.variables[st.session_state['time']]
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


def extract_dimensions(files_upload):

    # Extracts info from the uploaded nc files
    if files_upload:
        dimensions = []

        for uploaded_file in files_upload:
            nc_file = nc.Dataset('in-memory', memory=uploaded_file.getvalue(), diskless=True)

            # Extract depth information from the first file
            dimensions = nc_file.dimensions

            nc_file.close()

    return dimensions


# Makes sure the data in the files have all necessary data requirements
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


def decrement_step_twice():
    decrement_step()
    decrement_step()


# Back Button that takes user to previous page (twice if on the visualization page)
def back_button():
    if st.session_state['current_step'] == 2:
        st.button("Back", on_click=decrement_step_twice)
    else:
        st.button("Back", on_click=decrement_step)


# Next button that takes user to next page if condition is met
def next_button(condition):
    st.button("Next", on_click=increment_step, disabled=not condition)


# Select box for user selecting which visualization option they want
# Added helper tools to give a description for each option
def visualization_selectbox():
    help_input = (
        # Heat Map Description
        "**Heat Map**  \n"
        "This tool is designed for visualizing a chosen variable by coloring each data point according to its value. "
        "Higher values are illustrated with warm colors like red, while lower values are shown in cooler colors "
        "like blue.  \n"
        
        # Empty line
        "  \n" 
        
        # Quiver Plot Description
        "**Quiver Plot**  \n"
        "This tool is designed for visualizing vector fields like ocean currents. Each arrows size and direction "
        "visualizes the flow's direction and velocity. This visualization requires the horizontal (u) and vertical (v) "
        "vectors.  \n"
    )
    selected_visualization = st.selectbox(
        "Visualization Option:",
        options=["Heat Map", "Quiver Plot"],
        index=None,  # Default to None
        placeholder="Select Visualization Option",
        help=help_input
    )
    return selected_visualization


# Selection for variable if heat map is chosen
# Added helper tool description
def variable_selectbox(variables_not_dimensions):
    help_input = (
        # Variable Description
        "Select a variable that represents a distinct measurable quantity in your dataset, containing data across "
        "various Latitude and Longitude coordinates."
    )
    selected_variable = st.selectbox(
        "Heat Map Variable:",
        options=variables_not_dimensions,
        index=None,  # Default to None
        placeholder="Select Variable",
        help=help_input
    )
    return selected_variable


# Selection for xvelocity (U component) if quiver plot is chosen
def xvelocity_selectbox(variables_not_dimensions):
    help_input = (
        # Variable Description
        "This variable captures the movement in the horizontal direction, typically representing the east-west "
        "component of the current. It helps determine the direction and velocity as currents move horizontally."
    )
    selected_xvelocity = st.selectbox(
        "Quiver Plot Horizontal (u) Variable:",
        options=variables_not_dimensions,
        index=None,  # Default to None
        placeholder="Select Horizontal (u) Variable",
        help=help_input
    )
    return selected_xvelocity


# Selection for yvelocity (V component) if quiver plot is chosen
def yvelocity_selectbox(variables_not_dimensions):
    help_input = (
        # Variable Description
        "This variable captures the movement in the vertical direction, typically representing the north-south "
        "component of the current. It helps determine the direction and velocity as currents move vertically."
    )
    selected_yvelocity = st.selectbox(
        "Select Vertical (v) Variable:",
        options=variables_not_dimensions,
        index=None,  # Default to None
        placeholder="Select Vertical (v) Variable",
        help=help_input
    )
    return selected_yvelocity


# Lets user change the time the visual is represented.
def time_selectbox(datetime_to_file_map, all_datetime_strings):
    # Display time select box
    if all_datetime_strings:
        selected_datetime_str = st.selectbox(
            "Time:",
            options=all_datetime_strings,
            index=0  # Default to the first option
        )
        associated_files = datetime_to_file_map[selected_datetime_str]
    else:
        st.write("No datetime values found.")
    return selected_datetime_str, associated_files


# Lets user change the depth the visual is represented.
def depth_slider(depth_levels):
    # Display depth slider
    if depth_levels is not None:
        selected_depth = st.slider("Depth", 0, depth_levels - 1, value=0)
        # st.write(f"Selected depth level: {selected_depth}")
    else:
        st.write("No depth information available.")
    return selected_depth


# Used to find which datetime the time variable is represented in an .nc file (accessible for different nc files)
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


# Creates a heat map with the variable selected for each latitude, longitude, selected time, and selected depth.
def heatmap(variables_not_dimensions, file_bytes, datetime_str, depth, variable):
    # Load the NetCDF file from bytes
    nc_file = nc.Dataset('in-memory', memory=file_bytes)

    try:
        # Convert the selected datetime string back to a datetime object
        selected_datetime = parse_datetime(datetime_str)

        # Find the index of the selected time
        time_var = nc_file.variables[st.session_state['time']]
        time_units = time_var.units
        selected_time_index = np.where(nc.num2date(time_var[:], units=time_units) == selected_datetime)[0][0]

        # Access the data for the selected variable
        data = nc_file.variables[variable]

        # Assuming the data structure is [time, depth, lat, lon]
        selected_data = data[selected_time_index, depth, :, :]

        # Get latitude and longitude values for plotting
        lat = nc_file.variables[st.session_state['lat']][:]
        lon = nc_file.variables[st.session_state['lon']][:]

        # Create the heatmap
        fig, ax = plt.subplots()
        c = ax.pcolormesh(lon, lat, selected_data, cmap='coolwarm')

        # Adjust color
        color = "white"

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


# Creates a Quiver Plot with the selected U and V for each latitude, longitude, selected time, and selected depth.
def quiverplot(variables_not_dimensions, file_bytes, datetime_str, depth, selected_xvelocity, selected_yvelocity):
    # Load the NetCDF file from bytes
    nc_file = nc.Dataset('in-memory', memory=file_bytes)

    try:
        # Convert the selected datetime string back to a datetime object
        selected_datetime = parse_datetime(datetime_str)

        # Find the index of the selected time
        time_var = nc_file.variables[st.session_state['time']]
        time_units = time_var.units
        selected_time_index = np.where(nc.num2date(time_var[:], units=time_units) == selected_datetime)[0][0]

        # Access the data for the selected u and v velocity variables
        u_data = nc_file.variables[selected_xvelocity][selected_time_index, depth, :, :]
        v_data = nc_file.variables[selected_yvelocity][selected_time_index, depth, :, :]

        # Ensure lat and lon are 2D arrays for quiver plotting
        lat = nc_file.variables[st.session_state['lat']][:]
        lon = nc_file.variables[st.session_state['lon']][:]
        Lon, Lat = np.meshgrid(lon, lat)

        # Optionally, reduce the density of arrows for clarity
        skip = (slice(None, None, 5), slice(None, None, 5))  # Adjust the slicing for desired arrow density
        u_data = u_data[skip]
        v_data = v_data[skip]
        Lon = Lon[skip]
        Lat = Lat[skip]

        # Setting up the plot with a dark background for white elements to stand out
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 7.5))
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

