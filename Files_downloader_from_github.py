import requests as req
from bs4 import BeautifulSoup as bs

html_text = req.get('https://github.com/karthickai/Linear-Regression').text

soup = bs(html_text)
files = soup.find_all('tr', class_="react-directory-row undefined")

for file in files:
    links = set(file.find_all('a', class_="Link--primary"))
    
    for link in links:
        link = 'https://raw.githubusercontent.com/'+ link.get('href').replace('blob/','')
        file_response = req.get(link)

        if req.get(link).status_code == 200:
            filename = link.split("/")[-1].replace("%20", " ")
            with open("Downloaded/"+filename, "wb") as f:
                f.write(file_response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {link}")
            print(f"Status code: {file_response.status_code}")