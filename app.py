import streamlit as st
from docx import Document
import re
import json

st.title("Smart Contract Data Extractor for D365 BC")
st.write("""
Upload a Word (.docx) contract. 
The Copilot-assisted extraction will parse the document and show ERP-ready JSON format.
""")

uploaded_file = st.file_uploader("Upload Word contract (.docx)", type=["docx"])

def read_docx(file):
    """Read text from uploaded .docx file"""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def copilot_extract_contract(text):
    """
    Mock 'Copilot-assisted' extraction logic.
    Replace this with Copilot suggestions for smarter parsing.
    """
    # Simple keyword/regex extraction
    fields = {
        "Seller": "",
        "Buyer": "",
        "Commodity": "",
        "Quantity": "",
        "Price": "",
        "Terms": "",
        "Dates": "",
        "Incoterms": "",
        "Payment terms": "",
        "Governing law": "",
        "Bank details": ""
    }

    # Example regex extraction
    for key in fields.keys():
        pattern = re.compile(rf"{key}[:\-]\s*(.+)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            fields[key] = match.group(1).strip()

    return fields

if uploaded_file:
    contract_text = read_docx(uploaded_file)
    st.subheader("Contract Preview")
    st.text_area("Preview", contract_text, height=300)

    if st.button("Extract Data for D365 BC"):
        extracted_data = copilot_extract_contract(contract_text)
        st.success("Data extracted successfully!")
        st.subheader("ERP-ready JSON:")
        st.json(extracted_data)
