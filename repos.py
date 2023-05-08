import json
import os
import sys
import time

import pandas as pd
import requests
from github import Github


def check_github_api_credentials(api_url, token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print(
            "Die angegebene GitHub API-URL und/oder der Token sind nicht korrekt. Bitte überprüfen Sie Ihre Eingaben.")
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


GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = "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"


check_git = check_github_api_credentials(GITHUB_API_URL, GITHUB_TOKEN)

def fork_and_analyze_repositories(df, github_token):
    # Authenticate with the GitHub API
    g = Github(github_token)

    # Get the authenticated user
    user = g.get_user()

    # Iterate through the DataFrame and fork repositories to your account
    forked_repos = []
    for index, row in df.iterrows():
        repo_url = row["Repository URL"]
        repo_name = repo_url.split("/")[-1]
        original_repo = g.get_repo(repo_url.replace("https://github.com/", ""))

        try:
            forked_repo = user.create_fork(original_repo)
            forked_repos.append(forked_repo)
            print(f"Forked {repo_url} to {forked_repo.html_url}")
        except Exception as e:
            print(f"Error forking {repo_url}: {e}")

    # Ensure SonarCloud is set up and connected to your GitHub account
    # For instructions, follow the SonarCloud documentation: https://sonarcloud.io/documentation/analysis/github/
    # Make sure the SONAR_TOKEN environment variable is set with your SonarCloud token

    sonar_token = os.environ["SONAR_TOKEN"]

    def fetch_analysis_results(project_key, sonar_token, language):
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
        }
        headers = {"Authorization": f"Token {sonar_token}"}

        response = requests.get(sonar_api_url, headers=headers, params=params)

        if response.status_code == 200:
            issues = response.json()["issues"]
            results = []

            for issue in issues:
                result = {
                    "project_key": project_key,
                    "rule": issue["rule"],
                    "message": issue["message"],
                    "component": issue["component"],
                    "severity": issue["severity"],
                }
                results.append(result)

            return results
        else:
            print(f"Error fetching analysis results for {project_key}: {response.status_code}")
            return []

    # Analyze the forked repositories with SonarCloud
    for forked_repo in forked_repos:
        # Configure the repository in SonarCloud
        # For instructions, follow the SonarCloud documentation: https://sonarcloud.io/documentation/analysis/setup-analysis/

        # Run the SonarCloud analysis using the sonar-scanner command line tool
        # For instructions, follow the SonarCloud documentation: https://sonarcloud.io/documentation/analysis/scan/sonarscanner/
        # Make sure the sonar-scanner tool is installed and available in your PATH

        clone_url = forked_repo.clone_url
        repo_name = forked_repo.name

        # Clone the repository
        os.system(f"git clone {clone_url}")

        # Run SonarCloud analysis
        os.system(f"sonar-scanner -Dsonar.projectKey={user.login}_{repo_name} -Dsonar.sources=. -Dsonar.host.url=https://sonarcloud.io -Dsonar.login={sonar_token}")

        # Clean up cloned repository
        os.system(f"rm -rf {repo_name}")

        print(f"SonarCloud analysis completed for {forked_repo.html_url}")

        # Analyze the forked repositories with SonarCloud
        all_results = []
        for forked_repo in forked_repos:
            # ... (previous code) ...

            # Fetch SonarCloud analysis results
            project_key = f"{user.login}_{repo_name}"
            results = fetch_analysis_results(project_key, sonar_token)
            all_results.extend(results)

            # Sleep for a while to avoid rate limiting issues
            time.sleep(60)

        return all_results

if not check_git:
    sys.exit()

language = input("Enter the programming language: ")
min_size = input("Enter the minimum code size (in KB): ")
max_size = input("Enter the maximum code size (in KB): ")
num_repos = input("Enter the number of repositories to search for: ")

df = search_repositories(language, min_size, max_size, num_repos, GITHUB_TOKEN)


results = fork_and_analyze_repositories(df, GITHUB_TOKEN, SONAR_TOKEN)
print(json.dumps(results, indent=2))


print(df)
