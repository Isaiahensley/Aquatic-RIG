import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
from io import BytesIO

# Generating PDF Function
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

# Feedback Page Structure
def feedback_page():
    
    # Title
    st.title("Website Feedback Form")

    # User Information Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>User Information</h3>", unsafe_allow_html=True)
        first_time_visitor = st.radio("Is this the first time you are visiting the website?", ["Yes", "No"])
        primary_reason = st.text_input("What is the PRIMARY reason you came to the site?")

    # Content Feedback Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Content Feedback</h3>", unsafe_allow_html=True)

        # Question 1:
        # Did you find what you needed?
        found_what_needed = st.radio("Did you find what you needed?", ["Yes, all of it", "Yes, some of it", "No, none of it"])
        additional_info = ""
        if found_what_needed == "No, none of it":
            additional_info = st.text_area("If you did not find any or all of what you needed, please tell us what information you were looking for.")
        ease_of_finding_info = st.radio("Please tell us how easy it is to find information on the site.", ["Very Easy", "Easy", "Average", "Difficult", "Very Difficult"])

        # Question 2:
        # How easy was it to navigate the website and interact with the data visualization tools?
        first_question = ""
        first_question = st.markdown("How easy was it to navigate the website and interact with the data visualization tools?")
        first_radio = st.radio("", ["Very Easy", "Easy", "Moderate", "Hard", "Very Hard"])

        # Question 3:
        # How was the website's loading speed and responsiveness? Did you enounter any technical issues?
        second_question = ""
        second_question = st.text_area("How was the website's loading speed and responsiveness? Did you enounter any technical issues?")

        # Question 4:
        # Was the NC files' data visualization effective and clarified?
        third_question = ""
        third_question = st.text_area("Was the NC files' data visualization effective and clarified?")

        # Question 5:
        # Were there any specific features that you found useful or lacking?
        fourth_question = ""
        fourth_question = st.text_area("Were there any specific features that you found useful or lacking?")
        
        # Question 6:
        # Is there anything you'd like to bring up about the website's design, aesthetics, and organization?
        fifth_question = ""
        fifth_question = st.text_area("Is there anything you'd like to bring up about the website's design, aesthetics, and organization?")

        # Question 7:
        # In your own words, how was your experience using the website?
        sixth_question = ""
        sixth_question = st.text_area("In your own words, how was your experience using the website?")

        # Question 8:
        # Any suggestions or ideas for enhancing the website?
        seventh_question = ""
        seventh_question = st.text_area("Any suggestions or ideas for enhancing the website?")
        
    # Overall Impression Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Overall Impression</h3>", unsafe_allow_html=True)

        # Create a Row with Radio Boxes using Columns and Markdown
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("a. " + st.radio("", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="a"))
        with col2:
            st.markdown("b. " + st.radio("", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="b"))
        with col3:
            st.markdown("c. " + st.radio("", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="c"))

        # Question 9:
        # What is the likelihood that you will visit the website again?
        likelihood_to_visit_again = st.selectbox("What is the likelihood that you will visit the website again?", ["Extremely likely", "Very likely", "Moderately likely", "Slightly likely", "Not at all likely"])
        additional_comments = st.text_area("Please add any comments you have for improving the website.")
        
        # Slider for Overall Satisfaction Rating
        st.write("Overall Satisfaction Rating:")
        st.write("Please rate your overall satisfaction with the website:")
        overall_satisfaction = st.slider('Select a rating:', min_value=1, max_value=5, step=1)
        
    # Contant Information Container
    with st.container():
        contant_info_markdown = ""
        email_address = ""
        contant_info_markdown = st.markdown("<h3 style='color: #0077cc;'>Contact Information</h3>")
        email_address = st.text_area("Email Address:")

    # User Demographics Container
    with st.container():
        user_demo = ""
        age = ""
        occupation = ""
        industry = ""
        user_demo = st.markdown("<h3 style='color: #0077cc;'>User Demographics: Optional</h3>")
        age = st.text_area("Age:")
        occupation = st.text_area("Occupation:")
        industry = st.text_area("Industry:")

    # Privacy and Data Usage Container
    with st.container():
        privacy_markdown = ""
        privacy_statement = ""
        privacy_markdown = st.markdown("<h3 style='color: #0077cc;'>Privacy and Data Usage</h3>")
        privacy_statement = st.markdown("We will use your feedback data and ensure that your responses will be kept confidential and used only for improving this website.")

    # Sending Feedback Function
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

    # Main Function
    if __name__ == "__main__":
        feedback_page()
