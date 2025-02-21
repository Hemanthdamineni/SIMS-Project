import requests as req
from bs4 import BeautifulSoup as bs
import lxml
import read_resume as read_resume

def Downloader(repo_link):
    html_text = req.get(repo_link).text

    soup = bs(html_text, 'lxml')
    files = soup.find_all('tr', class_="react-directory-row undefined")

    for file in files:
        links = set(file.find_all('a', class_="Link--primary"))
        
        for link in links:
            link = 'https://raw.githubusercontent.com/'+ link.get('href').replace('blob/','')
            file_response = req.get(link)

            if req.get(link).status_code == 200:
                filename = link.split("/")[-1].replace("%20", " ")
                with open("Resume_Scrapper/Downloaded/"+filename, "wb") as f:
                    f.write(file_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {link}")
                print(f"Status code: {file_response.status_code}")

if __name__ == "__main__":  
    pdf_path = "Resume_Scrapper/Resume.pdf"

    resume_text, extracted_links = read_resume.extract_text_and_links_from_pdf(pdf_path)
    
    print(f"Extractd Text: {resume_text}")

    print("Extracted Links:")
    for link in extracted_links:
        print(link)
    print("\n")
    
    for link in extracted_links:
        if "github" in link:
            Downloader(link)