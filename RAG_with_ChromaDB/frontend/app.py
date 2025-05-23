import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()


API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("  Q&A Retrieval-Augmented Generation (RAG) with ChromaDB")


st.header("Upload PDF File")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Uploading and Indexing ..."):
        files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_URL}/upload-data", files=files)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.json()['error']}")
st.header("Ask a Question")
query_text = st.text_input("Enter your question:")
if st.button("Submit"):
    if query_text:
        with st.spinner("Fetching response ..."):
            response = requests.post(f"{API_URL}/query", params={"query_text": query_text})
            if response.status_code == 200:
                result = response.json()
                st.markdown(f"**Answer:** {result['content']}")
                st.markdown("**Sources:**")
                for source in result["sources"]:
                    st.markdown(f"- {source}")
            else:
                st.error("Error fetching response.")
    else:
        st.warning("Please enter a question.")
