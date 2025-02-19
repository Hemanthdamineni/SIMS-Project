import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            text += page_text 
    return text

resume_text = extract_text_from_pdf("Resume.pdf")
print(resume_text)
