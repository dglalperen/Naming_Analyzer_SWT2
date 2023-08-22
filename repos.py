from utils import check_github_api_credentials
import sys
import pandas as pd
import requests


def get_default_branch(repo_full_name, github_token):
    api_url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    else:
        print(f"Problem beim Abrufen des Standardbranches von {repo_full_name}")
        return "main"


def count_python_files(repo_full_name, github_token, max_lines_per_file):
    default_branch = get_default_branch(repo_full_name, github_token)
    api_url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"

    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        tree = response.json()["tree"]
        return sum(
            1
            for item in tree
            if item["path"].endswith(".py")
            and item.get("size", 0) <= max_lines_per_file
        )
    else:
        print(f"Problem beim Abrufen des Inhalts von {repo_full_name}")
        return 0


def search_repositories(
    language,
    min_size,
    max_size,
    num_repos,
    max_py_files,
    max_lines_per_file,
    year,
    github_token,
):
    min_size = int(min_size) * 1024  # Konvertiere KB in Bytes
    max_size = int(max_size) * 1024  # Konvertiere KB in Bytes
    num_repos = int(num_repos)

    api_url = "https://api.github.com/search/repositories"
    query = f"language:Python size:{min_size}..{max_size} created:>{year}-01-01"

    params = {
        "q": query,
        "sort": "stars",
        "order": "asc",
        "per_page": 100,
    }  # Sort by least stars first
    headers = {"Authorization": f"token {github_token}"}

    filtered_repos = []
    page_num = 1

    while len(filtered_repos) < num_repos:
        params["page"] = page_num
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Fehlercode: {response.status_code}")
            print(f"Fehlernachricht: {response.text}")
            print(
                "Es gab ein Problem beim Abrufen der Repositories. Bitte überprüfen Sie Ihre Eingaben und versuchen Sie es erneut."
            )
            return None

        repos = response.json()["items"]

        # Sofort abbrechen, wenn keine weiteren Ergebnisse vorhanden sind
        if not repos:
            break

        for repo in repos:
            if len(filtered_repos) >= num_repos:
                break
            py_files_count = count_python_files(
                repo["full_name"], github_token, max_lines_per_file
            )  # Pass the new parameter
            if py_files_count <= max_py_files:
                filtered_repos.append(repo)

        page_num += 1

    repo_urls = [repo["html_url"] for repo in filtered_repos]

    # Erstellen Sie einen Pandas DataFrame mit den Repository-URLs
    df = pd.DataFrame(repo_urls, columns=["Repository URL"])

    # Speichern Sie das DataFrame in einer CSV-Datei
    df.to_csv("repositories.csv", index=False)

    print(
        "Die Repositories wurden erfolgreich in der Datei 'repositories.csv' gespeichert."
    )
    return df


if __name__ == "__main__":
    GITHUB_API_URL = "https://api.github.com"
    GITHUB_TOKEN = "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"

    if not check_github_api_credentials(GITHUB_API_URL, GITHUB_TOKEN):
        sys.exit()

    language = input("Enter the programming language: ")
    min_size = input("Enter the minimum code size (in KB): ")
    max_size = input("Enter the maximum code size (in KB): ")
    num_repos = input("Enter the number of repositories to search for: ")
    max_py_files = int(input("Enter the maximum number of .py files in a repository: "))
    year = input("Enter the starting year for repository search: ")

    max_lines_per_file = int(
        input("Enter the maximum number of lines a .py file can contain: ")
    )

    df = search_repositories(
        language,
        min_size,
        max_size,
        num_repos,
        max_py_files,
        max_lines_per_file,
        year,
        GITHUB_TOKEN,
    )

    print(df)
