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


def count_python_files(repo_full_name, github_token, max_lines_per_file, max_py_files):
    default_branch = get_default_branch(repo_full_name, github_token)
    api_url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"

    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        tree = response.json()["tree"]
        py_files_count = sum(
            1
            for item in tree
            if item["path"].endswith(".py")
            and item.get("size", 0) <= int(max_lines_per_file)
        )

        # Überprüfen, ob die Anzahl der Python-Dateien und die maximale Zeilenzahl den gegebenen Beschränkungen entspricht
        return py_files_count <= int(max_py_files)
    else:
        print(f"Problem beim Abrufen des Inhalts von {repo_full_name}")
        return False


def search_repositories(
    language,
    min_size,
    max_size,
    num_repos,
    max_py_files,
    max_lines_per_file,
    year,
    last_updated_year,  # Neues Argument hinzufügen
    query_terms,  # Neues Argument hinzufügen
    github_token,
):
    min_size = int(min_size) * 1024  # Konvertiere KB in Bytes
    max_size = int(max_size) * 1024  # Konvertiere KB in Bytes
    num_repos = int(num_repos)

    api_url = "https://api.github.com/search/repositories"
    query = (f"language:{language} size:{min_size}..{max_size} created:>{year} {query_terms}"  # last_updated_year hinzufügen
        # query_terms hinzufügen
          )
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
        print('test')
        params["page"] = page_num
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Fehlercode: {response.status_code}")
            print(f"Fehlernachricht: {response.text}")
            print(
                "Es gab ein Problem beim Abrufen der Repositories. Bitte überprüfen Sie Ihre Eingaben und versuchen Sie es erneut."
            )
            print("Beenden...")
            return None

        repos = response.json()["items"]

        # Sofort abbrechen, wenn keine weiteren Ergebnisse vorhanden sind
        if not repos:
            print('Break')
            break

        for repo in repos:
            if len(filtered_repos) >= num_repos:
                break
            py_files_count = count_python_files(
                repo["full_name"], github_token, max_lines_per_file, max_py_files
            )  # Pass the new parameter
            if py_files_count:
                filtered_repos.append(repo)

        page_num += 1
    print('len', len(filtered_repos))
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
    """
    language = input("Enter the programming language: ")
    min_size = input("Enter the minimum code size (in KB): ")
    max_size = input("Enter the maximum code size (in KB): ")
    num_repos = input("Enter the number of repositories to search for: ")
    max_py_files = int(input("Enter the maximum number of .py files in a repository: "))
    year = input("Enter the starting year for repository search: ")
    last_updated_year = input("Enter the last updated year for repository search: ")
    search_terms = input("Enter specific search terms (e.g. test, demo, tutorial): ").split(",")
    query_terms = " ".join([f"-{term.strip()}" for term in search_terms])
       max_lines_per_file = int(
        input("Enter the maximum number of lines a .py file can contain: ")
    )
    """
    language = "Python"
    min_size = "100"
    max_size = "10000"
    num_repos = '20'
    max_py_files = '5'
    year = '2014'
    last_updated_year = '2016'
    search_terms = ['test, example, first']
    query_terms = " OR ".join(search_terms)

    max_lines_per_file = '200'


    df = search_repositories(
        language,
        min_size,
        max_size,
        num_repos,
        max_py_files,
        max_lines_per_file,
        year,
        last_updated_year,  # Neuen Parameter hinzufügen
        query_terms,  # Neuen Parameter hinzufügen
        GITHUB_TOKEN,
    )

    print(df)
