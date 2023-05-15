import sys
from sonar_analyzer import analyze_naming_conventions
from helpers import check_tools_exist, search_github_repositories
from get_most_used_language import get_most_used_language

"""
if __name__ == '__main__':

    
    check_tools_exist()

    choice = input("Choose an option:\n"
                   "1. Analyze a specific GitHub URL\n"
                   "2. Search for multiple repositories with specific characteristics\n"
                   "Enter 1 or 2: ")

    if choice == "1":
        repo_url = input("Enter the GitHub repository URL: ")
        language = get_most_used_language(repo_url)
        print("language", language)
        analyze_naming_conventions(repo_url, "javascript")
    elif choice == "2":
        language = input("Enter the programming language: ")
        min_size = input("Enter the minimum code size (in KB): ")
        max_size = input("Enter the maximum code size (in KB): ")
        num_repos = input("Enter the number of repositories to search for: ")

        repo_urls = search_github_repositories(language, num_repos)
        for repo_url in repo_urls:
            analyze_naming_conventions(repo_url, language)
    else:
        print("Invalid option. Please enter either 1 or 2.")
        sys.exit(1)
    
    """


import os
import subprocess
import sys

def main():
    # Variablen aus Argumenten lesen
    token = 'debe78c7993526771fbb2e040b98c93333094b48'
    organisation = "dglalperen"
    sonarcloud_url = "https://sonarcloud.io"
    project_key = "kaan_test" # Ändern Sie dies auf den tatsächlichen Projektschlüssel

    # SonarScanner-Konfiguration
    with open('sonar-project.properties', 'w') as f:
        f.write(f"""
        sonar.projectKey={project_key}
        sonar.organization={organisation}
        sonar.sources=./test.py
        sonar.host.url={sonarcloud_url}
        sonar.login={token}
        sonar.python.coverage.reportPaths=coverage.xml
        """)

    # Codeanalyse starten
    subprocess.run(["sonar-scanner"], check=True)

if __name__ == "__main__":
    main()

'''
df = pd.read_csv('repositories.csv')
analyze_naming_conventions(df, "javascript")
'''


# Bewertung in GPT 3.5
# Verbesserung in GPT 4
