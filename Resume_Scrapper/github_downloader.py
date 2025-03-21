import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional

def download_github_repo(repo_link: str) -> List[Tuple[str, bytes]]:
    """
    Downloads files from a GitHub repository and returns them as a list of tuples.
    
    Args:
        repo_link: URL to the GitHub repository
        
    Returns:
        List of tuples (file_name, file_content) for all downloadable files
    """
    repo_owner_name = repo_link.split("/")[-2]
    repo_name = repo_link.split("/")[-1]
    branch = "main"  # Default branch
    
    try:
        # First, try to determine the default branch
        api_url = f"https://api.github.com/repos/{repo_owner_name}/{repo_name}"
        response = requests.get(api_url)
        if response.status_code == 200:
            repo_info = response.json()
            branch = repo_info.get("default_branch", "main")
    except Exception:
        # If API fails, we'll continue with the assumed 'main' branch
        pass
    
    # Get repository file structure
    file_paths = get_repo_file_paths(repo_link, branch)
    
    # Download each file
    downloadable_files = []
    for file_path in file_paths:
        raw_url = f"https://raw.githubusercontent.com/{repo_owner_name}/{repo_name}/{branch}/{file_path}"
        file_response = requests.get(raw_url)

        if file_response.status_code == 200:
            file_name = file_path.split("/")[-1]
            downloadable_files.append((file_name, file_response.content))
        else:
            print(f"Failed to download: {file_path}")

    return downloadable_files

def get_repo_file_paths(repo_link: str, branch: str = "main") -> List[str]:
    """
    Gets all file paths from a GitHub repository.
    
    Args:
        repo_link: URL to the GitHub repository
        branch: Repository branch (default: 'main')
        
    Returns:
        List of file paths in the repository
    """
    try:
        response = requests.get(repo_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        path = repo_link[repo_link.index(".com/") + 5:]
        
        # Find links to files
        links = soup.find_all('a', class_="Link--primary", href=True)
        links = [link['href'] for link in links]

        file_paths = []
        for link in links:
            if "/blob/" in link:
                file_path = link.replace(f"{path}/blob/{branch}/", "")
                if file_path.startswith("/"):
                    file_path = file_path[1:]
                file_paths.append(file_path)
            elif "/tree/" in link and not link.endswith(f"/{branch}"):
                # Handle subdirectories recursively
                subdir_link = "https://github.com" + link
                subdir_files = get_repo_file_paths(subdir_link, branch)
                file_paths.extend(subdir_files)
                
        return list(set(file_paths))
    
    except Exception as e:
        print(f"Error getting repository file structure: {e}")
        return []