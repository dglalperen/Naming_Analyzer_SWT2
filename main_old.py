import os
import sys
import subprocess
import shutil
from urllib.parse import urlparse
import requests
import base64
from helpers import check_tools_exist

SONAR_HOST_URL = "https://sonarcloud.io"
SONAR_API_URL = f"{SONAR_HOST_URL}/api"
SONAR_LOGIN = "debe78c7993526771fbb2e040b98c93333094b48"
SONAR_ORGANIZATION = "dglalperen"
METRICS = 'bugs,code_smells,vulnerabilities,coverage'



def clone_repo(url, repo_dir):
    try:
        subprocess.run(['git', 'clone', url, repo_dir], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to clone the repository: {url}")
        sys.exit(1)

def analyze_code(repo_dir):
    try:
        subprocess.run([
            'sonar-scanner',
            f'-Dsonar.host.url={SONAR_HOST_URL}',
            f'-Dsonar.login={SONAR_LOGIN}',
            f'-Dsonar.organization={SONAR_ORGANIZATION}',
            f'-Dsonar.projectKey={SONAR_ORGANIZATION}:{os.path.basename(repo_dir)}',
            f'-Dsonar.projectBaseDir={repo_dir}'
        ], cwd=repo_dir, check=True)
    except subprocess.CalledProcessError:
        print("SonarScanner analysis failed.")
        sys.exit(1)

def cleanup(repo_dir):
    try:
        shutil.rmtree(repo_dir)
    except FileNotFoundError:
        pass

def fetch_project_metrics(project_key):
    token_encoded = base64.b64encode(f"{SONAR_LOGIN}:".encode()).decode()
    headers = {
        "Authorization": f"Basic {token_encoded}"
    }
    params = {
        'component': project_key,
        'metricKeys': METRICS
    }

    response = requests.get(f"{SONAR_API_URL}/measures/component", headers=headers, params=params)

    if response.status_code == 200:
        measures = response.json()['component']['measures']
        return {measure['metric']: measure['value'] for measure in measures}
    else:
        print(f"Failed to fetch project metrics. Status code: {response.status_code}")
        sys.exit(1)








def analyze_repository(repo_url):

    language_rules = {
        "java": "squid:S00100,squid:S00116,squid:S00117",
        "javascript": "javascript:S100,javascript:S101",
        "python": "python:S1542,python:S100",
        "csharp": "csharpsquid:S100,csharpsquid:S101",
        "php": "php:S116,php:S117",
        "ruby": "ruby:S100,ruby:S101",
    }
    # Check if the provided URL is a valid GitHub repository
    if not urlparse(repo_url).netloc == 'github.com':
        print("Invalid GitHub repository URL.")
        sys.exit(1)

    repo_name = urlparse(repo_url).path.split('/')[-1]
    repo_dir = os.path.join(os.getcwd(), repo_name)
    project_key = f"{SONAR_ORGANIZATION}:{repo_name}"

    cleanup(repo_dir)
    clone_repo(repo_url, repo_dir)
    analyze_code(repo_dir)
    cleanup(repo_dir)

    print(f"\nSonarCloud analysis completed for {repo_url}.")

    # Fetch and print the project metrics
    metrics = fetch_project_metrics(project_key)
    print("\nAnalysis Results:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
    print("\n")

def main():
    check_tools_exist()

    choice = input("Choose an option:\n"
                   "1. Analyze a specific GitHub URL\n"
                   "2. Search for multiple repositories with specific characteristics\n"
                   "Enter 1 or 2: ")

    if choice == "1":
        repo_url = input("Enter the GitHub repository URL: ")
        analyze_repository(repo_url)
    elif choice == "2":
        language = input("Enter the programming language: ")
        min_size = input("Enter the minimum code size (in KB): ")
        max_size = input("Enter the maximum code size (in KB): ")
        num_repos = input("Enter the number of repositories to search for: ")

        repo_urls = search_github_repositories(language,num_repos)
        for repo_url in repo_urls:
            analyze_repository(repo_url)
    else:
        print("Invalid option. Please enter either 1 or 2.")
        sys.exit(1)

if __name__ == '__main__':
    main()

