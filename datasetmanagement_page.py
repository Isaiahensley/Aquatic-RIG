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


initialize_state()


# Define steps for the workflow
def increment_step():
    st.session_state['current_step'] += 1


def decrement_step():
    if st.session_state['current_step'] > 0:
        st.session_state['current_step'] -= 1


# Main function to manage the dataset page
def dataset_management_page():

    # ------------------------
    # Step 0: File Upload Page
    # ------------------------

    if st.session_state['current_step'] == 0:
        st.session_state['files_upload'] = file_uploader()
        next_button(st.session_state['files_upload'])

    # Proceed if files are uploaded
    if st.session_state['files_upload']:
        all_datetime_strings, depth_levels, variables_not_dimensions, datetime_to_file_map = extract_file_data(st.session_state['files_upload'])

        # -----------------------------------
        # Step 1: Visualization Selection Page
        # -----------------------------------

        if st.session_state['current_step'] == 1:

            # Visualization Selection box
            selected_visualization = visualization_selectbox()

            # Create columns that let the next and back buttons display side by side.
            left, right, filler = st.columns([1, 1, 19])

            # If a visualization option is chosen...
            if selected_visualization != "None":
                st.session_state['selected_visualization'] = selected_visualization

            # Put Next button on the right (after condition is met)
            # This will take you to the Variable Selection Page
            with right:
                next_button(selected_visualization != "None")

            # Put Back button on the left
            # This will take you to the File Upload Page
            with left:
                back_button()

        # -------------------------------
        # Step 2: Variable Selection Page
        # -------------------------------

        if st.session_state.current_step == 2 and 'selected_visualization' in st.session_state:

            # If Heat Map is selected...
            if st.session_state.selected_visualization == "Heat Map":

                # Ask user to select variable for heat map
                selected_variable = variable_selectbox(variables_not_dimensions)

                # Create columns that let the next and back buttons display side by side.
                left, right, filler = st.columns([1, 1, 19])

                # If a variable has been selected...
                if selected_variable != "None":
                    st.session_state.selected_variable = selected_variable

                # Put Next button on the right (after variable is selected)
                # This will take you to the Visualize Page (Heat Map)
                with right:
                    next_button(selected_variable != "None")

            elif st.session_state.selected_visualization == "Quiver Plot":
                selected_xvelocity = xvelocity_selectbox(variables_not_dimensions)
                selected_yvelocity = yvelocity_selectbox(variables_not_dimensions)

                # Create columns that let the next and back buttons display side by side.
                left, right, filler = st.columns([1, 1, 19])

                if selected_xvelocity != "None" and selected_yvelocity != "None" and selected_xvelocity != selected_yvelocity:
                    st.session_state.selected_xvelocity = selected_xvelocity
                    st.session_state.selected_yvelocity = selected_yvelocity

                # Put Next button on the right (after variable is selected)
                # This will take you to the Visualize page (Quiver Plot)
                with right:
                    next_button(selected_xvelocity != "None" and selected_yvelocity != "None" and selected_xvelocity != selected_yvelocity)

            # Put Back button on the left
            # This will take you to the Visualization Selection Page
            with left:
                back_button()

        # --------------------------
        # Step 3: Visualize Page
        # --------------------------

        if st.session_state.current_step == 3:

            # This creates left column (1/3 screen) and right column (2/3) screen
            left_column, right_column = st.columns([1, 3])
            with left_column:
                selected_datetime_str, associated_files = time_selectbox(datetime_to_file_map, all_datetime_strings)
                selected_depth = depth_slider(depth_levels)
                st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
                back_button()
            if associated_files:
                file_content = next(
                    (file.getvalue() for file in st.session_state.files_upload if file.name == associated_files[0]),
                    None)

                # Create Heat Map based on variable selected
                if st.session_state.selected_visualization == "Heat Map" and 'selected_variable' in st.session_state:
                    with right_column:
                        heatmap(variables_not_dimensions, file_content, selected_datetime_str, selected_depth, st.session_state.selected_variable)

                # Create Quiver Plot based on U and V variables selected
                elif st.session_state.selected_visualization == "Quiver Plot" and 'selected_xvelocity' in st.session_state and 'selected_yvelocity' in st.session_state:
                    with right_column:
                        quiverplot(variables_not_dimensions, file_content, selected_datetime_str, selected_depth, st.session_state.selected_xvelocity, st.session_state.selected_yvelocity)

            # This will take you to the Variable Selection Page
            #with left_column:
                #placeholder1 = st.empty()
                #back_button()


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


def back_button():
    st.button("Back", on_click=decrement_step)


def next_button(condition):
    st.button("Next", on_click=increment_step, disabled=not condition)


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
        options=["None", "Heat Map", "Quiver Plot"],
        index=0,  # Default to the first option
        help=help_input
    )
    return selected_visualization


def variable_selectbox(variables_not_dimensions):
    help_input = (
        # Variable Description
        "Select a variable that represents a distinct measurable quantity in your dataset, containing data across "
        "various Latitude and Longitude coordinates."
    )
    selected_variable = st.selectbox(
        "Select Variable:",
        options=["None"] + variables_not_dimensions,
        index=0,  # Default to the first option
        help=help_input
    )
    return selected_variable

def xvelocity_selectbox(variables_not_dimensions):
    help_input = (
        # Variable Description
        "This variable captures the movement in the horizontal direction, typically representing the east-west "
        "component of the current. It helps determine the direction and velocity as currents move horizontally."
    )
    selected_xvelocity = st.selectbox(
        "Select Horizontal (u) Variable:",
        options=["None"] + variables_not_dimensions,
        index=0,  # Default to the first option
        help=help_input
    )
    return selected_xvelocity

def yvelocity_selectbox(variables_not_dimensions):
    help_input = (
        # Variable Description
        "This variable captures the movement in the vertical direction, typically representing the north-south "
        "component of the current. It helps determine the direction and velocity as currents move vertically."
    )
    selected_yvelocity = st.selectbox(
        "Select Vertical (v) Variable:",
        options=["None"] + variables_not_dimensions,
        index=0,  # Default to the first option
        help=help_input
    )
    return selected_yvelocity

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


def depth_slider(depth_levels):
    # Display depth slider
    if depth_levels is not None:
        selected_depth = st.slider("Depth", 0, depth_levels - 1, value=0)
        # st.write(f"Selected depth level: {selected_depth}")
    else:
        st.write("No depth information available.")
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


