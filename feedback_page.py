import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data):
    pdf_filename = "feedback_report.pdf"
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(100, 750, "Feedback Report")

    y_position = 730
    for key, value in data.items():
        pdf_canvas.drawString(100, y_position, f"{key}: {value}")
        y_position -= 15

    pdf_canvas.save()
    return pdf_filename

def feedback_page():
    st.title("Website Feedback Form")

    st.markdown("<h3 style='color: #0077cc;'>User Information</h3>", unsafe_allow_html=True)
    first_time_visitor = st.radio("Is it the first time you are visiting the website?", ["Yes", "No"])
    primary_reason = st.text_input("What is the PRIMARY reason you came to the site?")
    overall_satisfaction = st.slider('Overall Satisfaction Rating:', min_value=1, max_value=5, step=1)

    st.markdown("<h3 style='color: #0077cc;'>Content Feedback</h3>", unsafe_allow_html=True)
    found_what_needed = st.radio("Did you find what you needed?", ["Yes, all of it", "Yes, some of it", "No, none of it"])
    additional_info = ""
    if found_what_needed == "No, none of it":
        additional_info = st.text_area(
            "If you did not find any or all of what you needed, please tell us what information you were looking for.")
    ease_of_finding_info = st.radio("Please tell us how easy it is to find information on the site.",
                                    ["Very Easy", "Easy", "Average", "Difficult", "Very Difficult"])

    st.markdown("<h3 style='color: #0077cc;'>Overall Impression</h3>", unsafe_allow_html=True)
    with st.columns(3):
        st.radio("Overall Impression (a):", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="a")
        st.radio("Overall Impression (b):", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="b")
        st.radio("Overall Impression (c):", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"], key="c")

    st.markdown("<h3 style='color: #0077cc;'>Likelihood to Visit Again</h3>", unsafe_allow_html=True)
    likelihood_to_visit_again = st.selectbox("Likelihood to Visit Again:", ["Extremely likely", "Very likely", "Moderately likely", "Slightly likely", "Not at all likely"])
    additional_comments = st.text_area("Additional Comments:")

    st.markdown("<h3 style='color: #0077cc;'>User Demographics: Optional</h3>", unsafe_allow_html=True)
    age = st.text_area("Age:")
    occupation = st.text_area("Occupation:")
    industry = st.text_area("Industry:")

    st.markdown("<h3 style='color: #0077cc;'>User Experience</h3>", unsafe_allow_html=True)
    user_experience = st.text_area("User Experience:")

    st.markdown("<h3 style='color: #0077cc;'>Contact Information</h3>", unsafe_allow_html=True)
    email_address = st.text_area("Email Address:")

    st.markdown("<h3 style='color: #0077cc;'>Privacy and Data Usage</h3>", unsafe_allow_html=True)
    st.markdown("We will use your feedback data and ensure that your responses will be kept confidential and used only for improving this website.")

    if st.button("SEND"):
        feedback_data = {
            "First Time Visitor": first_time_visitor,
            "Primary Reason For Visiting": primary_reason,
            "Overall Satisfaction Rating": overall_satisfaction,
            "Found What Needed": found_what_needed,
            "Additional Information": additional_info,
            "Ease of Finding Information": ease_of_finding_info,
            "Overall Impression (a)": st.session_state.a,
            "Overall Impression (b)": st.session_state.b,
            "Overall Impression (c)": st.session_state.c,
            "Likelihood to Visit Again": likelihood_to_visit_again,
            "Additional Comments": additional_comments,
            "Age": age,
            "Occupation": occupation,
            "Industry": industry,
            "User Experience": user_experience,
            "Email Address": email_address,
        }
        pdf_filename = generate_pdf(feedback_data)
        st.markdown("### Generated PDF:")
        st.success("Thank you for your feedback! 🚀")

if __name__ == "__main__":
    feedback_page()
