import streamlit as st
from PIL import Image


def home_page():
    # Sidebar
    st.sidebar.markdown("Dataset-Related Links")
    st.sidebar.link_button("GitHub Page", "https://github.com/Isaiahensley/Aquatic-RIG")

    st.sidebar.markdown("Software-Related Links")
    st.sidebar.link_button("Matplotlib", "https://matplotlib.org/")
    st.sidebar.link_button("Streamlit", "https://streamlit.io/")
    st.sidebar.link_button("NumPy", "https://numpy.org/")

    # Main Content
    left_col, right_col = st.columns(2)
    with left_col:
        image = Image.open('AquaRigLogo.png')
        st.image(image, width=400, output_format="PNG")

    right_col.title('**:blue[Aquatic Rig]**')
    right_col.markdown("Created by Isaiah Hensley, Maria Black, Sudeep Paudel, Richard Peters")
    right_col.markdown("Louisiana State University Shreveport")

    st.divider()

    # Using containers to manage layout more flexibly
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.header('**:blue[Summary]**')
            st.write('Aquatic data researchers need a powerful and easy to use data visualization tool to sort through'
                     ' complex data. What makes our website tool different from others is the way it handles'
                     ' multi-dimensional data. Unlike existing software, our website lets users visualize several types'
                     ' of data at different coordinates dynamically for any given time and depth in the water. '
                     'While changing between water depths and time, our website provides real-time image generation'
                     ' allowing fast and easy understanding of how these several dimensions affect the data points.'
                     ' Our website focuses on visualizing aquatic data stored in NetCDF4 files. These files are '
                     'powerful for aquatic research as they allow data to be stored at specific'
                     ' multi-dimensional locations.')
            st.markdown("---")

            st.header("**:blue[Navigation]**")
            # Add navigation content here

        # GIFs in the third column
        with col3:
            st.header('**:blue[Data Visualization Examples:]** ')
            st.image("gif1.gif")
            st.caption("Ocean current velocities at different depths.")
            st.image("gif2.gif")
            st.caption("Temperature at different depths.")