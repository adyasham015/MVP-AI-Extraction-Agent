import streamlit as st
import requests
from docx import Document
import json

# --- Streamlit UI ---
st.title("Contract Extraction MVP")
uploaded_file = st.file_uploader("Upload contract (.docx)", type=["docx", "pdf"])

# --- Helper to read DOCX ---
def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# --- Call Foundry project ---
def call_foundry(contract_text):
    endpoint = "https://test-dea-resource.services.ai.azure.com/api/projects/test-dea"
    headers = {
        "Ocp-Apim-Subscription-Key": st.secrets["FOUNDARY_API_KEY"],  # put API key in Streamlit secrets
        "Content-Type": "application/json"
    }
    payload = {
        "input_text": contract_text
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Foundry API error {response.status_code}: {response.text}")
        return {}

# --- Main ---
if uploaded_file:
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        contract_text = read_docx(uploaded_file)
    else:
        st.warning("Currently only DOCX is supported")
        contract_text = ""

    st.subheader("Contract Preview")
    st.text_area("Preview", contract_text, height=300)

    if st.button("Extract Data"):
        with st.spinner("Calling Foundry AI Agent..."):
            extracted_data = call_foundry(contract_text)
        st.subheader("ERP-ready JSON")
        st.json(extracted_data)

        if st.button("Send to ERP"):
            # mock API call
            st.success("Data sent to ERP (mock)!")
