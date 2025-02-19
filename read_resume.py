import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                page_text = page_text.replace('\n', ' \n')  
                text += page_text + "\n"  
    return text

resume_text = extract_text_from_pdf("me.pdf")
print(resume_text)
