import streamlit as st
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Function to convert CV to JSON
def cv_to_json(cv_text):
    cv_lines = cv_text.split('\n')
    cv_data = {}

    for line in cv_lines:
        if line.startswith("Name:"):
            cv_data["name"] = line.split(":")[1].strip()
        elif line.startswith("Contact:"):
            cv_data["contact"] = line.split(":")[1].strip()
        elif line.startswith("Education:"):
            cv_data["education"] = line.split(":")[1].strip()
        elif line.startswith("Experience:"):
            cv_data["experience"] = line.split(":")[1].strip()
        elif line.startswith("Skills:"):
            cv_data["skills"] = [skill.strip() for skill in line.split(":")[1].split(",")]

    return json.dumps(cv_data, indent=4)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Streamlit app
st.title("Mentor-Mentee CV Similarity Checker")

# Upload CVs
mentee_cv_file = st.file_uploader("Upload Mentee's CV (PDF)", type=["pdf"])
mentor_cv_file = st.file_uploader("Upload Mentor's CV (PDF)", type=["pdf"])

if st.button("Compare CVs"):
    if mentee_cv_file and mentor_cv_file:
        # Extract text from PDFs
        mentee_cv = extract_text_from_pdf(mentee_cv_file)
        mentor_cv = extract_text_from_pdf(mentor_cv_file)

        # Convert CVs to JSON
        mentee_cv_json = cv_to_json(mentee_cv)
        mentor_cv_json = cv_to_json(mentor_cv)

        # Convert CVs to a list for vectorization
        cvs = [mentee_cv, mentor_cv]

        # Vectorize the CVs using TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(cvs)

        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # Extract the similarity score between the mentee and mentor CVs
        similarity_score = similarity_matrix[0][1]

        st.write("### Mentee CV JSON")
        st.json(mentee_cv_json)

        st.write("### Mentor CV JSON")
        st.json(mentor_cv_json)

        st.write(f"### Similarity Score: {similarity_score:.2f}")

    else:
        st.write("Please upload both CVs to compare.")


