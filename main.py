from rate_repository import rate_repository_semantic
from syntactic_score import rate_repository_syntactic
from utils import clone_repo, delete_repo, check_github_api_credentials
import nltk
import pandas as pd
import os
from improve_repository import improve_and_evaluate_repositories

if __name__ == "__main__":
    GITHUB_API_URL = "https://api.github.com"
    github_token = "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"
    gpt4_key = "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"
    gpt3_key = "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"

    if github_token is None or gpt4_key is None or gpt3_key is None:
        print("Please set the necessary environment variables.")
        exit(1)

    # Load the CSV into a DataFrame
    repositories_df = pd.read_csv("repositories.csv")

    # falls rates.csv nicht exisitert soll der code ausgeführt werden
    if not os.path.exists("rates.csv"):
        repositories_df["Semantic Rating"] = None
        repositories_df["Syntactic Rating"] = None

        for index, row in repositories_df.iterrows():
            repo_url = row["Repository URL"]
            try:
                if check_github_api_credentials(GITHUB_API_URL, github_token):
                    python_files = clone_repo(repo_url, github_token)
                    repo_name = "/".join(repo_url.split("/")[-2:])
                    syntactic_score = rate_repository_syntactic(repo_name)
                    semantic_score = rate_repository_semantic(python_files, gpt4_key)
                    score = {**syntactic_score, **semantic_score}
                    print(
                        "der Score für das das Repo: "
                        + repo_url
                        + " ist: "
                        + str(score)
                    )
                    repositories_df.at[index, "Semantic Rating"] = score[
                        "semantic_score"
                    ]
                    repositories_df.at[index, "Syntactic Rating"] = score[
                        "syntactic_score"
                    ]
                    # delete repository
                    delete_repo(repo_url)
                else:
                    print(f"Github API credentials are not valid for repo {repo_url}")
            except Exception as e:
                print(f"Error occurred during the evaluation of repo {repo_url}: {e}")

        # Save the updated DataFrame to a CSV
        repositories_df.to_csv("rates.csv", index=False)

    improve_and_evaluate_repositories(gpt3_key, gpt4_key, github_token)
