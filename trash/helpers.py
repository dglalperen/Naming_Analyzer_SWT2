import sys
import subprocess
import requests
import urllib.parse

# CONSTANTS --> später auslagern in env vars
SONAR_ORGANIZATION = "dglalperen"
SONAR_TOKEN = "debe78c7993526771fbb2e040b98c93333094b48"
GITHUB_TOKEN = "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"
GITHUB_API_URL = "https://api.github.com"
def check_tools_exist():
    tools = ['git', 'sonar-scanner']
    for tool in tools:
        try:
            subprocess.run([tool, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print(f"{tool} not found. Please ensure it is installed and in your PATH.")
            sys.exit(1)

def get_repo_language(repo_url):
    api_base_url = "https://api.github.com/repos/"

    # Extract user and repo name from the URL
    try:
        user, repo_name = repo_url.split("github.com/")[1].split("/", 1)
    except IndexError:
        return "Invalid GitHub repository URL."

    repo_name = repo_name.rstrip("/")

    # Construct the API URL and make a request
    api_url = f"{api_base_url}{user}/{repo_name}"
    response = requests.get(api_url)

    if response.status_code != 200:
        return f"Error {response.status_code}: Unable to fetch repository information."

    repo_data = response.json()

    # Extract the programming language used in the repository
    language = repo_data.get("language", "Unknown")

    return language

def get_api_url(github_url):
    parsed_url = urllib.parse.urlparse(github_url)
    repo_path = parsed_url.path
    base_api_url = "https://api.github.com/repos"
    api_url = f"{base_api_url}{repo_path}"
    return api_url

def search_github_repositories(language, num_repos):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    params = {
        "q": f"language:{language}",
        "per_page": num_repos,
        "sort": "stars",  # Optional: sort the results by the number of stars
        "order": "desc"   # Optional: order the results in descending order
    }

    response = requests.get(f"{GITHUB_API_URL}/search/repositories", headers=headers, params=params)

    if response.status_code == 200:
        items = response.json()['items']
        return [item['html_url'] for item in items]
    else:
        print(f"Failed to search for repositories. Status code: {response.status_code}")
        sys.exit(1)