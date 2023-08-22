import csv
import os
import glob
from github import Github
from git import Repo

from rate_repository import rate_repository_semantic
from semantic_evaluation import request_code_improvement
import pandas as pd
from utils import clone_repo


def improve_repository(repo_link, openai_token, github_token):
    # Create a global directory for all improved repositories
    global_improved_dir = os.path.join(os.getcwd(), "improved_repos")
    os.makedirs(global_improved_dir, exist_ok=True)

    # Clone the repository using the provided function and get all Python files
    python_files = clone_repo(repo_link, github_token)

    # Create a directory for the improved repository inside the global directory
    repo_name = os.path.basename(repo_link)
    improved_repo_dir = os.path.join(global_improved_dir, f"improved_{repo_name}")
    os.makedirs(improved_repo_dir, exist_ok=True)

    # Iterate over the Python files and improve them
    for file in python_files:
        with open(file, "r") as f:
            code_snippet = f.read()

        improved_code = request_code_improvement(code_snippet, openai_token)
        if improved_code:  # Save the improved code if it's not None or empty
            # Save the improved code in the improved repository directory
            improved_file_path = os.path.join(improved_repo_dir, os.path.basename(file))
            with open(improved_file_path, "w") as f:
                f.write(improved_code)

    return improved_repo_dir


def improve_and_evaluate_repositories(gpt3_token, gpt4_token, github_token):
    # Read the Repository URLs from the CSV file
    with open("repositories.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        repo_urls = [row[0] for row in reader]

    # DataFrame to hold the results
    results_df = pd.DataFrame(columns=["Repository URL", "Semantic Score"])

    # Improve and evaluate each repository
    for repo_url in repo_urls:
        print(f"Improving and evaluating repository: {repo_url}")

        # Improve the repository using GPT-3 token and get the directory of improved files
        improved_dir = improve_repository(repo_url, gpt3_token, github_token)

        # Find all improved .py files
        os.chdir(improved_dir)
        improved_python_files = glob.glob("**/*.py", recursive=True)

        # Evaluate the improved repository with the GPT-4 token
        rating = rate_repository_semantic(improved_python_files, gpt4_token)

        # Add the results to the DataFrame
        results_df = results_df.append(
            {"Repository URL": repo_url, "Semantic Score": rating["semantic_score"]},
            ignore_index=True,
        )

    # Save the results to a new CSV file
    results_df.to_csv("improved_repositories_ratings.csv", index=False)

    print("Improvement and evaluation process completed!")
