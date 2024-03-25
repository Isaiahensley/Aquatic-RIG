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

    # Overall Impression Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Overall Impression</h3>", unsafe_allow_html=True)
        was_easy_navigate = st.radio("Was the website easy to navigate?", ["Yes", "No"], index=None)
        was_homepage_informative = st.radio("Did you find the home page informative?", ["Yes", "No"], index=None)
        was_data_manage_intuitive = st.radio("Did you find the dataset management page intuitive to use?",
                                             ["Yes", "No"], index=None)
        was_about_page_informative = st.radio("Did you find the about page informative?", ["Yes", "No"], index=None)

    # NetCDF4 Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>NetCDF4</h3>", unsafe_allow_html=True)
        have_used_net_files = st.radio("Have you ever used NetCDF4 files before?", ["Yes", "No"], index=None)
        upload_own_files = st.radio("Did you upload your own files or use the example dataset?",
                                    ["I uploaded my own files.", "I used the example dataset."], index=None)

    # Data Visualization Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Data Visualization</h3>", unsafe_allow_html=True)
        useful_visual = st.radio("Do you think the visualizations generated are useful?", ["Yes", "No"], index=None)
        useful_features = st.text_area("Which specific features or aspects of the visualizations did you find most "
                                       "useful or interesting?")
        confusing_features = st.radio("Are there any features or aspects of the visualizations that you found "
                                      "confusing or unnecessary?", ["Yes", "No"], index=None)
        if confusing_features == "Yes":
            what_confusing = st.text_area("What did you find confusing or unnecessary?")
        suggestions_visual = st.text_area("Do you have any suggestions for improving the visualizations generated in"
                                          "the dataset management page?")

    # Performance Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Performance</h3>", unsafe_allow_html=True)
        performance_question = st.text_area("How was the website's loading speed and responsiveness? Did you encounter"
                                            "any technical issues?")

    # User Information Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>User Information</h3>", unsafe_allow_html=True)
        email_address = st.text_input("Email:")
        if email_address == "":
            st.warning("Please enter email address.")
        is_student = st.radio("Are you a student?", ["Yes", "No"], index=None)
        if is_student == "Yes":
            field_of_study = st.text_input("What is your Field of Study?")
            if field_of_study == "":
                st.warning("Please enter field of study.")

    # Additional Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Additional</h3>", unsafe_allow_html=True)
        additional_comments = st.text_area("Please share any additional comments or suggestions you have for us.")

    # Privacy and Data Usage Container
    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>Privacy and Data Usage</h3>", unsafe_allow_html=True)
        st.markdown("We will use your feedback data and ensure that your responses will be used "
                    "only for improving this website.")

    # Sending Feedback Function
    if st.button("SEND"):
        # Generate PDF
        feedback_data = {
            "Was Easy to Navigate": was_easy_navigate,
            "Was Homepage Informative": was_homepage_informative,
            "Was Data Management Page Intuitive": was_data_manage_intuitive,
            "Was About Page Informative": was_about_page_informative,
            "Has User Used NetCDF4 Files Before": have_used_net_files,
            "Is User's Own Files": upload_own_files,
            "Is Visualization Useful": useful_visual,
            "Useful Features in Visualization": useful_features,
            "Confusing Parts for Visualization": what_confusing,
            "Suggestions for Visuals": suggestions_visual,
            "Feedback Performance": performance_question,
            "Email Address": email_address,
            "Field of Study": field_of_study,
            "Additional Comments": additional_comments
        }
        pdf_filename = generate_pdf(feedback_data)

        # Display success message
        st.markdown("### Generated PDF:")
        st.success("Thank you for your feedback! 🚀")

    # Main Function
    if __name__ == "__main__":
        feedback_page()