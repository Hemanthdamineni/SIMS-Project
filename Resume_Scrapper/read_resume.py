import pdfplumber
import pdfminer.high_level as pm

def extract_text_and_links_from_pdf(pdf_path):
    text = pm.extract_text(pdf_path)
    links = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            hyperlinks = page.hyperlinks
            if hyperlinks:
                for hyperlink in hyperlinks:
                    if 'uri' in hyperlink:
                        links.append(hyperlink['uri'])
    
    return text, links