import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1) Open the terminal in the bottom left of PyCharm.
# 2) Type "pip install streamlit"
# 3) run streamlitPractice.py by right-clicking it at the top and select Run
# 4) To open the streamlit application in your browser:
# 4a) Open the terminal again and type "python -m streamlit run streamlitPractice.py"
# 4b) If that does not work use it tells you to when you run the python file and copy that into your terminal

# Now you should have a streamlit website running in your browsers!
# Everytime you make changes to this code and run it, you can go back to that website and select rerun to update it

# Answer the questions in the following code statements. After this
def main():
    # Put your name here
    st.title("Sudeep Paudel")

    # What are .nc files used for and how is the data stored?
    st.write("Nc files refers to NetCDF files used for saving climate data in multi dimensions(array oriented scientific data) ")

    # What is spatio temporal data?
    st.write("Spatio Temporal data refers to data related to both space and time.")

    # Take a look at the matPlot generated on the website. It's generated from a simple csv file with temperature
    # readings at various x and y coordinates. How would things become complicated if the dataset also had another
    # dimension "z"? Then also imagine this data was all collected over and over again every hour. How could we
    # visualize data like this?
    st.write("If the dataset also had **another dimension 'z'** in addition to the x and y coordinates, "
             "*then z might represent something like the depth of the water.* If the data was collected over and over "
             "again every hour we might visualize the data by adding a feature that allows users to *adjust through "
             "times by the hour.*")

def matPlot():
    # Load CSV data into a DataFrame
    df = pd.read_csv("WaterTemperatureDataset.csv")

    # Extract X, Y, and Temp values
    X = df['X']
    Y = df['Y']
    Temp = df['Temp']

    # Reshape data for contour plot
    X = X.values.reshape((10, 10))
    Y = Y.values.reshape((10, 10))
    Temp = Temp.values.reshape((10, 10))

    # Display contour plot
    fig, ax = plt.subplots()
    contour = ax.contourf(X, Y, Temp, cmap='viridis')
    plt.colorbar(contour, ax=ax, label='Temperature')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Display the plot in Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
    matPlot()
