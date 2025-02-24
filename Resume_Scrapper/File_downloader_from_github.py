import requests
from bs4 import BeautifulSoup

def Downloader(repo_link, base_path="Resume_Scrapper/Downloaded/code_files/"):
    branch = "main"  # Change to "master" if needed

    # Step 1: Get all file paths
    response = requests.get(repo_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    path = repo_link[repo_link.index(".com/") + 5:]
    
    links = soup.find_all('a', class_="Link--primary", href=True)
    links = [link['href'] for link in links]

    files = []
    for link in links:
        if "/blob/" in link:
            file_path = link.replace(f"{path}/blob/{branch}/", "")
            files.append(file_path)
        elif "/tree/" in link:
            Downloader("https://github.com" + link)
            
    files = set(files)  # Remove duplicates

    # Step 2: Download each file
    for file in files:
        raw_url = f"https://github.com/{file}"
        file_response = requests.get(raw_url)
        folder = raw_url.split("/")[-2]

        if file_response.status_code == 200:
            with open(base_path + folder + "-"+ file.split("/")[-1], "wb") as f:
                f.write(file_response.content)
            print(f"Downloaded: {file}")
        else:
            print(f"Failed to download: {file}")