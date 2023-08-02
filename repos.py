import glob
from github import Github
from git import Repo
import os
import sys
import pandas as pd
import requests
import shutil

def check_github_api_credentials(api_url, token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print(
            "Die angegebene GitHub API-URL und/oder der Token sind nicht korrekt. Bitte überprüfen Sie Ihre Eingaben.")
        print(response.status_code)
        return False


def search_repositories(language, min_size, max_size, num_repos, github_token):
    if min_size == '-':
        min_size = 1000
    if max_size == '-':
        max_size = 100000

    min_size = int(min_size) * 1024  # Konvertiere KB in Bytes
    max_size = int(max_size) * 1024  # Konvertiere KB in Bytes
    num_repos = int(num_repos)

    api_url = "https://api.github.com/search/repositories"
    query = f"language:{language} size:{min_size}..{max_size}"

    if min_size != 1000:
        query += f" size:>{min_size}"
    if max_size != 100000:
        query += f" size:<{max_size}"


    params = {"q": query, "sort": "stars", "order": "desc", "per_page": num_repos}

    headers = {"Authorization": f"token {github_token}"}  # Ersetzen Sie YOUR_GITHUB_TOKEN mit Ihrem persönlichen Token
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        repos = response.json()["items"]
        repo_urls = [repo["html_url"] for repo in repos]

        # Erstellen Sie einen Pandas DataFrame mit den Repository-URLs
        df = pd.DataFrame(repo_urls, columns=["Repository URL"])

        # Speichern Sie das DataFrame in einer CSV-Datei
        df.to_csv("repositories.csv", index=False)

        print("Die Repositories wurden erfolgreich in der Datei 'repositories.csv' gespeichert.")
        return df
    else:
        print("Es gab ein Problem beim Abrufen der Repositories. Bitte überprüfen Sie Ihre Eingaben und versuchen Sie es erneut.")
        return None


def clone_repo(repo_link, github_token):
    # Get repo name from the link
    repo_name = "/".join(repo_link.split("/")[-2:])

    # Initialize Github instance with your token
    g = Github(github_token)

    # Get repo instance
    repo = g.get_repo(repo_name)

    # Define repo directory
    repo_dir = os.path.abspath(f'./repos/{repo_name}')

    # Check if the repository already exists. If so, delete it before cloning again.
    if os.path.exists(repo_dir):
        print(f"Repository {repo_name} already exists. Deleting and cloning again.")
        shutil.rmtree(repo_dir)

    # Clone the repository
    Repo.clone_from(repo_link, repo_dir)

    # Get all Python files in the repository
    python_files = glob.glob(os.path.join(repo_dir, '**/*.py'), recursive=True)

    return python_files


def delete_repo(repo_link):
    # Get repo name from the link
    repo_name = "/".join(repo_link.split("/")[-2:])

    # Define repo directory
    repo_dir = os.path.abspath(f'./repos/{repo_name}')

    # Check if the repository exists. If so, delete it.
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
        print(f"Repository {repo_name} deleted.")
    else:
        print(f"Repository {repo_name} does not exist.")







GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = "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"


check_git = check_github_api_credentials(GITHUB_API_URL, GITHUB_TOKEN)



if not check_git:
    sys.exit()
"""
language = input("Enter the programming language: ")
min_size = input("Enter the minimum code size (in KB): ")
max_size = input("Enter the maximum code size (in KB): ")
num_repos = input("Enter the number of repositories to search for: ")

df = search_repositories(language, min_size, max_size, num_repos, GITHUB_TOKEN)

print(df)
"""

