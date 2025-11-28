import streamlit as st
from docx import Document
from openai import OpenAI
import json

st.title("Smart Contract Data Extractor for D365 BC")
st.write("""
Upload a Word (.docx) contract. 
The AI connector will extract key fields and show them in ERP-ready JSON format.
""")

# --- OpenAI client using Streamlit secrets ---
client = OpenAI(api_key=st.secrets["OPEN_API_KEY"])

# --- Helper function to read .docx ---
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# --- AI extraction ---
def ai_extract_contract(text):
    prompt = f"""
You are a contract extraction engine.
Extract the following fields as JSON only:

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

Contract text:
{text}

Return ONLY JSON. No explanation.
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # or gpt-4
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error("Could not parse JSON from AI response.")
        return {}

# --- Streamlit interface ---
uploaded_file = st.file_uploader("Upload Word contract (.docx)", type=["docx"])

if uploaded_file:
    contract_text = read_docx(uploaded_file)
    st.subheader("Contract Preview")
    st.text_area("Preview", contract_text, height=300)

    if st.button("Extract Data for D365 BC"):
        with st.spinner("Extracting data using OpenAI..."):
            extracted_data = ai_extract_contract(contract_text)
        st.success("Data extracted successfully!")
        st.subheader("ERP-ready JSON:")
        st.json(extracted_data)
