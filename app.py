def copilot_extract_contract(text):
    """
    Improved keyword-based extraction.
    Finds each field keyword and extracts text following it until a line break or next keyword.
    """
    fields = ["Seller", "Buyer", "Commodity", "Quantity", "Price",
              "Terms", "Dates", "Incoterms", "Payment terms", 
              "Governing law", "Bank details"]
    
    extracted = {field: "" for field in fields}
    
    # Split text into lines for easier processing
    lines = text.split("\n")
    
    for i, line in enumerate(lines):
        for field in fields:
            # Case-insensitive match for field keyword
            if field.lower() in line.lower():
                # Extract text after colon or dash if exists
                parts = line.split(":")
                if len(parts) > 1:
                    value = ":".join(parts[1:]).strip()
                else:
                    parts = line.split("-")
                    value = parts[1].strip() if len(parts) > 1 else ""
                
                # If value is empty, try the next line
                if not value and i + 1 < len(lines):
                    value = lines[i+1].strip()
                
                # Save the value
                extracted[field] = value
                
    return extracted
