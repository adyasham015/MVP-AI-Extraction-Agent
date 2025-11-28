import streamlit as st
from docx import Document
import openai
import os
import json

# --- Streamlit page ---
st.title("Smart Contract Data Extractor for D365 BC")
st.write("""
Upload a Word (.docx) contract. 
The AI connector will extract key fields and show them in ERP-ready JSON format.
""")

# --- OpenAI API Key (set as environment variable) ---
openai.api_key = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload Word contract (.docx)", type=["docx"])

def read_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def ai_extract_contract(text):
    """
    Sends contract text to OpenAI GPT to extract structured data
    """
    prompt = f"""
You are a contract data extraction assistant. 
Extract the following fields from the contract text below in JSON format:

- Seller
- Buyer
- Commodity
- Quantity
- Price
- Terms
- Dates
- Incoterms
- Payment terms
- Governing law
- Bank details

Contract Text:
{text}

Return ONLY JSON with keys exactly as listed.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    try:
        extracted_json = response.choices[0].message.content.strip()
        return json.loads(extracted_json)
    except Exception as e:
        st.error("Failed to parse JSON from AI response.")
        return {}

if uploaded_file:
    contract_text = read_docx(uploaded_file)
    st.subheader("Contract Preview")
    st.text_area("Preview", contract_text, height=300)

    if st.button("Extract Data for D365 BC"):
        with st.spinner("Extracting data using AI..."):
            extracted_data = ai_extract_contract(contract_text)
        st.success("Data extracted successfully!")
        st.subheader("ERP-ready JSON:")
        st.json(extracted_data)
