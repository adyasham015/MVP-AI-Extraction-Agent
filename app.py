import streamlit as st
import re
import json

# --- Mock document extractor ---
def mock_extract_contract(text):
    """Simulates Azure Form Recognizer output"""
    # Simple regex examples; in real life you'd call LLM or OCR
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

# --- Streamlit App ---
st.title("Contract Data Extractor MVP")

uploaded_file = st.file_uploader("Upload your contract (.txt for MVP)", type=["txt"])

if uploaded_file:
    contract_text = uploaded_file.read().decode("utf-8")
    
    st.subheader("Raw Contract Text")
    st.text_area("Contract Content", contract_text, height=200)
    
    # Extract data
    extracted_data = mock_extract_contract(contract_text)
    
    st.subheader("Extracted Data")
    form = st.form(key="kyc_form")
    
    seller = form.text_input("Seller", extracted_data.get("Seller"))
    buyer = form.text_input("Buyer", extracted_data.get("Buyer"))
    commodity = form.text_input("Commodity", extracted_data.get("Commodity"))
    quantity = form.text_input("Quantity", extracted_data.get("Quantity"))
    price = form.text_input("Price", extracted_data.get("Price"))
    terms = form.text_input("Terms", extracted_data.get("Terms"))
    dates = form.text_input("Dates", extracted_data.get("Dates"))
    incoterms = form.text_input("Incoterms", extracted_data.get("Incoterms"))
    payment = form.text_input("Payment terms", extracted_data.get("Payment terms"))
    law = form.text_input("Governing law", extracted_data.get("Governing law"))
    bank = form.text_input("Bank details", extracted_data.get("Bank details"))
    
    submit = form.form_submit_button("Send to ERP")
    
    if submit:
        # Simulate API POST
        payload = {
            "Seller": seller,
            "Buyer": buyer,
            "Commodity": commodity,
            "Quantity": quantity,
            "Price": price,
            "Terms": terms,
            "Dates": dates,
            "Incoterms": incoterms,
            "Payment terms": payment,
            "Governing law": law,
            "Bank details": bank
        }
        st.success("Data sent to ERP (simulated)")
        st.json(payload)
