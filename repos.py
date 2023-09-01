from utils import check_github_api_credentials
import sys
import pandas as pd
import requests
import tiktoken
import base64

def num_tokens_from_string(string: str, encoding_name: str) -> int:

    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_default_branch(repo_full_name, github_token):
    api_url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    else:
        print(f"Problem beim Abrufen des Standardbranches von {repo_full_name}")
        return "main"


def get_file_content(repo_full_name, filename, github_token):
    api_url = f"https://api.github.com/repos/{repo_full_name}/contents/{filename}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)
    try:
        content_decoded = base64.b64decode(response.json()["content"]).decode("utf-8")
    except UnicodeDecodeError:
        return 'x' * 10000
    if response.status_code == 200:
        return content_decoded
    else:
        return None


def count_python_tokens(repo_full_name, github_token, max_tokens):
    default_branch = get_default_branch(repo_full_name, github_token)
    api_url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{default_branch}?recursive=1"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        tree = response.json()["tree"]
        total_tokens = 0
        for item in tree:
            if item["path"].endswith(".py"):
                file_content = get_file_content(repo_full_name, item["path"], github_token)
                if file_content:
                    total_tokens += num_tokens_from_string(file_content, "gpt-3.5-turbo")

        return total_tokens <= int(max_tokens)
    else:
        print(f"Problem beim Abrufen des Inhalts von {repo_full_name}")
        return False

def search_repositories(
    language,
    num_repos,
    year,
    max_tokens,
    query_terms,
    github_token,
):
    num_repos = int(num_repos)

    api_url = "https://api.github.com/search/repositories"
    query = f"language:{language} created:{year} {query_terms}"  # last_updated_year hinzufügen


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
            py_files_count = count_python_tokens(
                repo["full_name"], github_token, max_tokens,
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

    language = "Python"
    num_repos = '10'
    max_tokens = '5000'
    year = '2022'
    last_updated_year = '2016'
    search_terms = ['test', 'example']
    query_terms = " OR ".join(search_terms)


    df = search_repositories(
        language,
        num_repos,
        year,
        max_tokens,
        query_terms,
        GITHUB_TOKEN,
    )

    print(df)
