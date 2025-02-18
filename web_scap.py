import requests
from bs4 import BeautifulSoup

repo_url = "https://github.com/Karthik0000007/Bagging"
"""
Happy to help you with this. I have written a Python script that can download all files from a GitHub repository.
"""
branch = "main"  # Change to "master" if needed

# Step 1: Get all file paths
response = requests.get(repo_url)
soup = BeautifulSoup(response.text, 'html.parser')

files = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.startswith(f"/Karthik0000007/Bagging/blob/{branch}/"):
        file_path = href.replace(f"/Karthik0000007/Bagging/blob/{branch}/", "")
        files.append(file_path)

# Step 2: Download each file
for file in files:
    raw_url = f"https://raw.githubusercontent.com/Karthik0000007/Bagging/{branch}/{file}"
    file_response = requests.get(raw_url)

    if file_response.status_code == 200:
        with open(file.split("/")[-1], "wb") as f:
            f.write(file_response.content)
        print(f"Downloaded: {file}")
    else:
        print(f"Failed to download: {file}")
