import csv
import os
import glob
from github import Github
from git import Repo

from rate_repository import rate_repository_semantic
from semantic_evaluation import request_code_improvement
import pandas as pd

from utils import clone_repo


def improve_repository(repo_link, openai_token):
    try:
        # Get repo name from the link
        repo_name = repo_link.split("/")[-1]

        # Initialize GitHub instance with your token
        g = Github(openai_token)

        # Get repo instance
        repo = g.get_repo(repo_name)

        # Clone the repository
        repo_dir = os.path.join(os.getcwd(), repo_name)
        Repo.clone_from(repo_link, repo_dir)

        # Find all .py files in the cloned repo
        os.chdir(repo_dir)
        python_files = glob.glob("**/*.py", recursive=True)

        # Create a new directory for improved files
        improved_dir = os.path.join(os.getcwd(), f"improved_{repo_name}")
        os.makedirs(improved_dir, exist_ok=True)

        # Iterate over the Python files and improve them
        for file in python_files:
            file_path = os.path.join(repo_dir, file)
            with open(file_path, "r") as f:
                code_snippet = f.read()
            try:
                improved_code = request_code_improvement(code_snippet, openai_token)
                if (
                    improved_code
                ):  # Only save the improved code if it's not None or empty
                    # Save the improved code in the new directory
                    improved_file_path = os.path.join(improved_dir, file)
                    with open(improved_file_path, "w") as f:
                        f.write(improved_code)
            except Exception as e:
                print(f"Error improving code in {file}: {e}")
    except Exception as e:
        print(f"Error processing repository: {e}")


def improve_and_evaluate_repositories(gpt3_token, gpt4_token, github_token):
    # Lesen Sie die Repository-URLs aus der CSV-Datei
    with open("repositories.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Überspringen Sie die Header-Zeile
        repo_urls = [row[0] for row in reader]

    # Leeres DataFrame für die Ergebnisse
    results_df = pd.DataFrame(columns=["Repository URL", "Semantic Score"])

    # Verbessern und bewerten Sie jedes Repository
    for repo_url in repo_urls:
        print(f"Improving and evaluating repository: {repo_url}")

        # Verbessern Sie das Repository mit dem GPT-3-Token
        improve_repository(repo_url, gpt3_token)

        # Clone the repository using the provided function and get all Python files
        python_files = clone_repo(repo_url, github_token)

        # Bewerten Sie das verbesserte Repository erneut mit dem GPT-4-Token
        rating = rate_repository_semantic(python_files, gpt4_token)

        # Fügen Sie die Ergebnisse dem DataFrame hinzu
        results_df = results_df.append(
            {"Repository URL": repo_url, "Semantic Score": rating["semantic_score"]},
            ignore_index=True,
        )

    # Speichern Sie die Ergebnisse in einer neuen CSV-Datei
    results_df.to_csv("improved_repositories_ratings.csv", index=False)

    print("Improvement and evaluation process completed!")
