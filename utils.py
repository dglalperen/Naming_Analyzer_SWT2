import shutil
import glob
from github import Github
from git import Repo
import os
import requests


def clone_repo(repo_link, github_token):
    # Get repo name from the link
    repo_name = "/".join(repo_link.split("/")[-2:])

    # Initialize Github instance with your token
    g = Github(github_token)

    # Get repo instance
    repo = g.get_repo(repo_name)

    # Define repo directory
    repo_dir = os.path.abspath(f'./repos/{repo_name}')

    # Check if the repository already exists
    if os.path.exists(repo_dir):
        print(f"Repository {repo_name} already exists. Using existing repo.")
    else:
        # If not, clone the repository
        print(f"Cloning repository {repo_name}.")
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


def check_github_api_credentials(api_url, token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print("Die angegebene GitHub API-URL und/oder der Token sind nicht korrekt. Bitte überprüfen Sie Ihre Eingaben.")
        print(response.status_code)
        return False