import streamlit as st
from docx import Document
import PyPDF2
import requests

st.title("Smart Contract Data Extractor for D365 BC")
st.write("""
Upload a Word (.docx) or PDF contract. 
The deployed agent will extract key fields and show ERP-ready JSON.
""")

# --- Streamlit secrets ---
api_key = st.secrets["FOUNDARY_API_KEY"]
agent_endpoint = st.secrets["FOUNDARY_AGENT_ENDPOINT"]

# --- Helper: read DOCX ---
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# --- Helper: read PDF ---
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

# --- Call Foundry Agent ---
def call_foundry(text):
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are an expert in extracting contract fields into ERP-ready JSON."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 1000
    }
    
    response = requests.post(agent_endpoint, headers=headers, json=payload)
    
    if response.status_code != 200:
        st.error(f"Foundry API error {response.status_code}: {response.text}")
        return {}
    
    try:
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", {})
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        return {}

# --- File uploader ---
uploaded_file = st.file_uploader("Upload contract (.docx or .pdf)", type=["docx", "pdf"])

if uploaded_file:
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        contract_text = read_docx(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        contract_text = read_pdf(uploaded_file)
    else:
        st.error("Unsupported file type")
        contract_text = ""

    st.subheader("Contract Preview")
    st.text_area("Preview", contract_text, height=300)

    if st.button("Extract Data for ERP"):
        with st.spinner("Extracting data from Foundry agent..."):
            extracted_data = call_foundry(contract_text)
        if extracted_data:
            st.success("Data extracted successfully!")
            st.subheader("ERP-ready JSON:")
            st.json(extracted_data)
            
            if st.button("Send to ERP (mock)"):
                st.info("Data would be sent to ERP here.")
