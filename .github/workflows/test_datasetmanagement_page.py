import streamlit as st
from datetime import datetime
import pytest
from unittest.mock import patch

from datasetvisualization_page.py import datasetmanagement_page

@pytest.fixture
def streamlit_dg_fixture():
    with patch("streamlit.DeltaGenerator") as mock_dg:
        yield mock_dg

def test_datasetmanagement_page(streamlit_dg_fixture):
    # Arrange
    mock_dg = streamlit_dg_fixture()
    # Simulate file upload
    mock_file_upload = "mocked_file_contents"
    with patch("streamlit.file_uploader", return_value=mock_file_upload):
        # Act
        datasetmanagement_page()

    # Assert
    mock_dg.title.assert_called_with("Dataset Management")
    mock_dg.file_uploader.assert_called_with("Upload dataset", type=["nc"])
    
    mock_dg.selectbox.assert_called_with(
        "How would you like this dataset visualized?",
        ("Scatter Plot", "Quiver", "Heat Map", "Contourf")
    )
    
    # Simulate sliders
    mock_dg.slider.assert_any_call("Time", value=datetime(2020, 1, 1, 9, 30), format="MM/DD/YY - hh:mm")
    mock_dg.slider.assert_any_call("Depth", 0, 100)
