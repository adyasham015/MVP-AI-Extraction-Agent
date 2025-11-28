# File: app.py
import streamlit as st
import re
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from docx import Document

# --- Mock document extractor ---
def mock_extract_contract(text):
    """Simulates Azure Form Recognizer output"""
    seller = re.search(r"Seller: (.+)", text)
    buyer = re.search(r"Buyer: (.+)", text)
    commodity = re.search(r"Commodity: (.+)", text)
    quantity = re.search(r"Quantity: (.+)", text)
    price = re.search(r"Price: (.+)", text)
    terms = re.search(r"Terms: (.+)", text)
    dates = re.search(r"Date: (.+)", text)
    incoterms = re.search(r"Incoterms: (.+)", text)
    payment = re.search(r"Payment: (.+)", text)
    law = re.search(r"Governing Law: (.+)", text)
    bank = re.search(r"Bank: (.+)", text)
    
    return {
        "Seller": seller.group(1) if seller else "",
        "Buyer": buyer.group(1) if buyer else "",
        "Commodity": commodity.group(1) if commodity else "",
        "Quantity": quantity.group(1) if quantity else "",
        "Price": price.group(1) if price else "",
        "Terms": terms.group(1) if terms else "",
        "Dates": dates.group(1) if dates else "",
        "Incoterms": incoterms.group(1) if incoterms else "",
        "Payment terms": payment.group(1) if payment else "",
        "Governing law": law.group(1) if law else "",
        "Bank details": bank.group(1) if bank else ""
    }

# --- Text extraction functions ---
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_excel(file):
    df = pd.read_excel(file, sheet_name=None)  # all sheets
    text = ""
    for sheet_name, sheet in df.items():
        sheet_text = sheet.astype(str).agg(' '.join, axis=1).str.cat(sep='\n')
        text += sheet_text + "\n"
    return text

# --- Streamlit App ---
st.title("Contract Data Extractor MVP")
st.write("Upload a contract (PDF, Word, Excel, or TXT)")

uploaded_file = st.file_uploader("Choose a contract", type=["txt","pdf","docx","xlsx"])

extracted_data = None

if uploaded_file:
    file_type = uploaded_file.type
    text = ""

    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        text = extract_text_from_excel(uploaded_file)
    
    st.text_area("Contract Preview", text, height=200)

    if st.button("Extract Data & Show ERP Format"):
        extracted_data = mock_extract_contract(text)
        st.success("Data extracted successfully!")
        st.subheader("Data ready to push to ERP:")
        st.json(extracted_data)
