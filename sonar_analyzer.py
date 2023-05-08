import json
import os
import time
import requests
from github import Github

def fetch_analysis_results(project_key, language):
    sonar_api_url = "https://sonarcloud.io/api/issues/search"

    language_rules = {
        "java": "squid:S00100,squid:S00116,squid:S00117",
        "javascript": "javascript:S100,javascript:S101",
        "python": "python:S1542,python:S100",
        "csharp": "csharpsquid:S100,csharpsquid:S101",
        "php": "php:S116,php:S117",
        "ruby": "ruby:S100,ruby:S101",
    }

    rules = language_rules.get(language.lower(), "")

    params = {
        "componentKeys": project_key,
        "rules": rules,
        "ps": 500,  # Page size
        "p": 1,  # Page number
        "organization": SONAR_ORGANIZATION,
    }
    headers = {"Authorization": f"Token {SONAR_TOKEN}"}

    response = requests.get(sonar_api_url, headers=headers, params=params)

    # ... (rest of the function remains unchanged) ...

def fork_and_analyze_repositories(df, language):
    # Authenticate with the GitHub API
    github = Github(GITHUB_TOKEN)

    # Get the authenticated user
    user = github.get_user()

    # Fork and clone the repositories from the DataFrame
    forked_repos = []
    all_results = []
    for index, row in df.iterrows():
        repo_url = row["Repository URL"]
        repo_owner, repo_name = repo_url.split("/")[-2:]

        # Fork the repository
        try:
            original_repo = github.get_repo(f"{repo_owner}/{repo_name}")
            forked_repo = user.create_fork(original_repo)
            forked_repos.append(forked_repo)
            print(f"Forked repository: {forked_repo.html_url}")
        except Exception as e:
            print(f"Error forking repository: {repo_url} - {str(e)}")
            continue

        # Clone the forked repository
        os.system(f"git clone {forked_repo.ssh_url}")

        # Change the working directory to the cloned repository
        os.chdir(repo_name)

        # Run SonarCloud analysis
        os.system(f"sonar-scanner -Dsonar.projectKey={user.login}_{repo_name} -Dsonar.sources=. -Dsonar.host.url=https://sonarcloud.io -Dsonar.login={SONAR_TOKEN} -Dsonar.organization={SONAR_ORGANIZATION}")

        # Fetch SonarCloud analysis results
        project_key = f"{user.login}_{repo_name}"
        results = fetch_analysis_results(project_key, SONAR_TOKEN, language, SONAR_ORGANIZATION)
        all_results.extend(results)

        # Change the working directory back to the parent directory
        os.chdir("..")

        # Remove the cloned repository folder
        os.system(f"rm -rf {repo_name}")

        # Sleep for a while to avoid rate limiting issues
        time.sleep(60)

    return all_results


SONAR_ORGANIZATION = "dglalperen"
SONAR_TOKEN = "debe78c7993526771fbb2e040b98c93333094b48"
GITHUB_TOKEN = "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"
