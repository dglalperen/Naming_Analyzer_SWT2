import os
import sys
import subprocess
import shutil
from urllib.parse import urlparse
import requests
import base64
import time

SONAR_HOST_URL = "https://sonarcloud.io"
SONAR_API_URL = f"{SONAR_HOST_URL}/api"
SONAR_LOGIN = "debe78c7993526771fbb2e040b98c93333094b48"
SONAR_ORGANIZATION = "dglalperen"
METRICS = 'bugs,code_smells,vulnerabilities,coverage'
REPO_URL = "https://github.com/dglalperen/skeleton-loader.git"

def check_tools_exist():
    tools = ['git', 'sonar-scanner']
    for tool in tools:
        try:
            subprocess.run([tool, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print(f"{tool} not found. Please ensure it is installed and in your PATH.")
            sys.exit(1)

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

if __name__ == '__main__':

    # Check if the provided URL is a valid GitHub repository
    if not urlparse(REPO_URL).netloc == 'github.com':
        print("Invalid GitHub repository URL.")
        sys.exit(1)

    check_tools_exist()

    repo_name = urlparse(REPO_URL).path.split('/')[-1]
    repo_dir = os.path.join(os.getcwd(), repo_name)
    project_key = f"{SONAR_ORGANIZATION}:{repo_name}"

    cleanup(repo_dir)
    clone_repo(REPO_URL, repo_dir)
    analyze_code(repo_dir)
    cleanup(repo_dir)

    print("SonarCloud analysis completed.")

    # Fetch and print the project metrics
    metrics = fetch_project_metrics(project_key)
    print("\nAnalysis Results:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
