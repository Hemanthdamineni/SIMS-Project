import requests as req
from bs4 import BeautifulSoup as bs
import lxml
import read_resume as read_resume

header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

def Downloader(repo_link):
    html_text = req.get(repo_link, headers=header).text

    soup = bs(html_text, 'lxml')
    files = soup.find_all('tr', class_="react-directory-row undefined")

    for file in files:
        links = set(file.find_all('a', class_="Link--primary"))
                
        for link in links:
            if "/tree/" in link:
                # folder = req.get('link', headers=header)
                # folder_links = folder.find_all('tr', class_="react-directory-row undefined")

                html_text_1 = req.get(link, headers=header).text
                soup_1 = bs(html_text_1, 'lxml')
                files_1 = soup_1.find_all('tr', class_="react-directory-row undefined")

                for file_1 in files_1:
                    links_1 = set(file_1.find_all('a', class_="Link--primary"))
                            
                    for link_1 in links_1:
                        if "/blob/" in link_1:
                            link_1 = 'https://raw.githubusercontent.com/'+ link_1.get('href').replace('blob/','')
                            file_response = req.get(link_1, headers=header)

                            if req.get(link_1).status_code == 200:
                                filename = link_1.split("/")[-1].replace("%20", " ")
                                with open("Resume_Scrapper/Downloaded/code_files/"+filename, "wb") as f:
                                    f.write(file_response.content)
                                print(f"Downloaded: {filename}")
                            else:
                                print(f"Failed to download: {link_1}")
                                print(f"Status code: {file_response.status_code}")

                
            if "/blob/" in link:
                link = 'https://raw.githubusercontent.com/'+ link.get('href').replace('blob/','')
                file_response = req.get(link, headers=header)

                if req.get(link).status_code == 200:
                    filename = link.split("/")[-1].replace("%20", " ")
                    with open("Resume_Scrapper/Downloaded/code_files/"+filename, "wb") as f:
                        f.write(file_response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download: {link}")
                    print(f"Status code: {file_response.status_code}")
