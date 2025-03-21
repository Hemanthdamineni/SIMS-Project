# import pdfplumber
# import fitz 
# import re
# from typing import Tuple, List

# def extract_text_and_links_from_pdf(pdf_path: str) -> Tuple[str, List[str]]:
#     """
#     Extracts text and links from a PDF file using PyMuPDF and PDFPlumber.
    
#     Args:
#         pdf_path: Path to the PDF file
        
#     Returns:
#         A tuple containing (text_content, list_of_links)
#     """
#     # Extract text and links using PyMuPDF for better performance
#     try:
#         doc = fitz.open(pdf_path)
#         text = ""
#         links = []
        
#         for page in doc:
#             text += page.get_text()
#             for link in page.get_links():
#                 if 'uri' in link:
#                     links.append(link['uri'])
        
#         # Also try to extract hyperlinks using PDFPlumber as a fallback
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 hyperlinks = page.hyperlinks
#                 if hyperlinks:
#                     for hyperlink in hyperlinks:
#                         if 'uri' in hyperlink:
#                             links.append(hyperlink['uri'])
        
#         # Find GitHub links in the text that might be missed
#         github_link_pattern = r"https://github\.com/[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+"
#         github_links = re.findall(github_link_pattern, text)
#         links.extend(github_links)
        
#         # Remove duplicates while preserving order
#         unique_links = []
#         for link in links:
#             if link not in unique_links:
#                 unique_links.append(link)
                
#         return text, unique_links
    
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return "", []

import pdfplumber
import pdfminer.high_level as pm
import re

def extract_text_and_links_from_pdf(pdf_path):
    try:
        text = pm.extract_text(pdf_path)
        links = []

        github_link_pattern = r"https://github\.com/[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+"
        links += re.findall(github_link_pattern, text)

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                hyperlinks = page.hyperlinks
                if hyperlinks:
                    for hyperlink in hyperlinks:
                        if 'uri' in hyperlink:
                            links.append(hyperlink['uri'])

        links = list(set(links))
        return text, links
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return "", []