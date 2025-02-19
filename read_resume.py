import pdfplumber

def extract_text_and_links_from_pdf(pdf_path):
    text = ""
    links = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            
            hyperlinks = page.hyperlinks
            if hyperlinks:
                for hyperlink in hyperlinks:
                    if 'uri' in hyperlink:
                        links.append(hyperlink['uri'])
    
    return text, links

