import streamlit as st

def feedback_form():
    st.title("Website Feedback Form")

    first_time_visitor = st.radio("Is this the first time you have visited the website?", ["Yes", "No"])

    primary_reason = st.text_input("What is the PRIMARY reason you came to the site?")

    found_what_needed = st.radio("Did you find what you needed?", ["Yes, all of it", "Yes, some of it", "No, none of it"])

    if found_what_needed == "No, none of it":
        additional_info = st.text_area("If you did not find any or all of what you needed, please tell us what information you were looking for.")

    ease_of_finding_info = st.radio("Please tell us how easy it is to find information on the site.", ["Very Easy", "Easy", "Average", "Difficult", "Very Difficult"])

    overall_impression = st.radio("What is your overall impression of the site?", ["Below Expectations", "Meets Expectations", "Exceeds Expectations"])

    professional_rating = st.slider("Professional", 0, 10, step=1)

    informative_rating = st.slider("Informative", 0, 10, step=1)

    visually_pleasing_rating = st.slider("Visually Pleasing", 0, 10, step=1)

    likelihood_to_visit_again = st.selectbox("What is the likelihood that you will visit the website again?", ["Extremely likely", "Very likely", "Moderately likely", "Slightly likely", "Not at all likely"])

    additional_comments = st.text_area("Please add any comments you have for improving the website.")

    if st.button("SEND"):
        # You can add code here to handle the form data, e.g., save it to a database or perform further analysis.
        st.success("Feedback submitted successfully!")

if __name__ == "__main__":
    website_feedback_form()

