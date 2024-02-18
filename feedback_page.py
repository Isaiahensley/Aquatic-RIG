import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
from io import BytesIO


def generate_pdf(data):
    pdf_filename = "feedback_report.pdf"
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)

    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(100, 750, "Feedback Report")

    # Add feedback data to the PDF
    y_position = 730
    for key, value in data.items():
        pdf_canvas.drawString(100, y_position, f"{key}: {value}")
        y_position -= 15

    pdf_canvas.save()
    return pdf_filename


def feedback_page():
    st.title("Website Feedback Form")

    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>User Information</h3>", unsafe_allow_html=True)
        first_time_visitor = st.radio("Is this the first time you have visited the website?", ["Yes", "No"])
        primary_reason = st.text_input("What is the PRIMARY reason you came to the site?")

        # Slider for overall satisfaction rating
        st.write("Overall Satisfaction Rating:")
        st.write("Please rate your overall satisfaction with the website:")
        overall_satisfaction = st.slider('Select a rating:', min_value=1, max_value=5, step=1)

    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Content Feedback</h3>", unsafe_allow_html=True)
        found_what_needed = st.radio("Did you find what you needed?", ["Yes, all of it", "Yes, some of it", "No, none of it"])
        additional_info = ""
        if found_what_needed == "No, none of it":
            additional_info = st.text_area("If you did not find any or all of what you needed, please tell us what information you were looking for.")
        ease_of_finding_info = st.radio("Please tell us how easy it is to find information on the site.", ["Very Easy", "Easy", "Average", "Difficult", "Very Difficult"])

    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Overall Impression</h3>", unsafe_allow_html=True)

        # Create a row with radio boxes using columns and Markdown
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("a. " + st.radio("", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="a"))
        with col2:
            st.markdown("b. " + st.radio("", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="b"))
        with col3:
            st.markdown("c. " + st.radio("", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="c"))

    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Likelihood to Visit Again</h3>", unsafe_allow_html=True)
        likelihood_to_visit_again = st.selectbox("What is the likelihood that you will visit the website again?", ["Extremely likely", "Very likely", "Moderately likely", "Slightly likely", "Not at all likely"])
        additional_comments = st.text_area("Please add any comments you have for improving the website.")

    # First Field
    with st.container():
        first_field = ""
        first_field_q = ""
        first_field = st.markdown("<h3 style='color: #0077cc;'>Ease of Use</h3>")
        first_field_q = st.markdown("How easy was it to navigate the website and interact with the data visualization tools?")
        first_radio = st.radio("", ["Very Easy", "Easy", "Moderate", "Hard", "Very Hard"])

    # Second Field
    with st.container():
        second_field = ""
        second_field_q = ""
        second_field = st.markdown("<h3 style='color: #0077cc;'>Design and Layout</h3>")
        second_field_q = st.text_area("Is there anything you'd like to bring up about the website's design, aesthetics, and organization?")

    # Third Field
    with st.container():
        third_field = ""
        third_field_q = ""
        third_field = st.markdown("<h3 style='color: #0077cc;'>Performance</h3>")
        third_field_q = st.text_area("How was the website's loading speed and responsiveness? Did you enounter any technical issues?")

    # Fourth Field
    with st.container():
        fourth_field = ""
        fourth_field_q = ""
        fourth_field = st.markdown("<h3 style='color: #0077cc;'>Data Visualization Quality</h3>")
        fourth_field_q = st.text_area("Were NC files' data visualization effective and clarified?")

    # Fifth Field
    with st.container():
        fifth_field = ""
        fifth_field_q = ""
        fifth_field = st.markdown("<h3 style='color: #0077cc;'>Features and Functionality</h3>")
        fifth_field_q = st.text_area("Were there any specific features that you found useful or lacking?")

    # Sixth Field
    with st.container():
        sixth_field = ""
        sixth_field_q = ""
        sixth_field = st.markdown("<h3 style='color: #0077cc;'>Suggestions for Improvement</h3>")
        sixth_field_q = st.text_area("Any suggestions or ideas for enhancing the website?")

    # Seventh Field
    with st.container():
        seventh_field = ""
        seventh_field_q1 = ""
        seventh_field_q2 = ""
        seventh_field_q3 = ""
        seventh_field = st.markdown("<h3 style='color: #0077cc;'>User Demographics: Optional</h3>")
        seventh_field_q1 = st.text_area("Age:")
        seventh_field_q2 = st.text_area("Occupation:")
        seventh_field_q3 = st.text_area("Industry:")

    # Eighth Field
    with st.container():
        eighth_field = ""
        eighth_field_q = ""
        eighth_field = st.markdown("<h3 style='color: #0077cc;'>User Experience</h3>")
        eighth_field_q = st.text_area("In your own words, how was your experience using the website?")

    # Ninth Field
    with st.container():
        ninth_field = ""
        ninth_field_q = ""
        ninth_field = st.markdown("<h3 style='color: #0077cc;'>Contact Information</h3>")
        ninth_field_q = st.text_area("Email Address:")

    # Tenth Field
    with st.container():
        tenth_field = ""
        tenth_field_q = ""
        tenth_field = st.markdown("<h3 style='color: #0077cc;'>Privacy and Data Usage</h3>")
        tenth_field_q = st.markdown("We will use your feedback data and ensure that your responses will be kept confidential and used only for improving this website.")

    if st.button("SEND"):
        # Generate PDF
        feedback_data = {
            "First Time Visitor": first_time_visitor,
            "Primary Reason For visiting the website": primary_reason,
            "Overall Satisfaction Rating": overall_satisfaction,
            "Found What Needed": found_what_needed,
            "Additional Info": additional_info,
            "Ease of Finding Info": ease_of_finding_info,
            "Overall Impression (a)": st.session_state.a,
            "Overall Impression (b)": st.session_state.b,
            "Overall Impression (c)": st.session_state.c,
            "Likelihood to Visit Again": likelihood_to_visit_again,
            "Additional Comments": additional_comments,
        }
        pdf_filename = generate_pdf(feedback_data)

        # Display success message
        st.markdown("### Generated PDF:")
        st.success("Thank you for your feedback! 🚀")

    if __name__ == "__main__":
        feedback_page()
