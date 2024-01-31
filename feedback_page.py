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

def feedback_form():
    st.title("Website Feedback Form")

    with st.container():
        st.markdown("<h3 style='color: #0077cc;'>User Information</h3>", unsafe_allow_html=True)
        first_time_visitor = st.radio("Is this the first time you have visited the website?", ["Yes", "No"])
        primary_reason = st.text_input("What is the PRIMARY reason you came to the site?")

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

    if st.button("SEND"):
        # Generate PDF
        feedback_data = {
            "First Time Visitor": first_time_visitor,
            "Primary Reason": primary_reason,
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

        # Display PDF
        with open(pdf_filename, "rb") as f:
            pdf_contents = f.read()

        # Convert PDF to base64 encoding
        pdf_base64 = base64.b64encode(pdf_contents).decode("utf-8")

        # Display download link
        st.markdown(f"### Generated PDF:")
        st.markdown(
            f'<a href="data:application/pdf;base64,{pdf_base64}" download="{pdf_filename}">Download PDF</a>',
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.write(pdf_filename)
        st.success("Thank you for your feedback! 🚀")

    if __name__ == "__main__":
        feedback_form()


