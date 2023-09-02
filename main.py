from syntactic_rate import rate_repository_syntactic
from utils import clone_repo, delete_repo, check_github_api_credentials
import nltk
import pandas as pd
import os
#from improve_repository import improve_and_evaluate_repositories
from openai_prompts import prompt_langchain


if __name__ == "__main__":
    GITHUB_API_URL = "https://api.github.com"
    github_token = "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"

    # Load the CSV into a DataFrame
    repositories_df = pd.read_csv("repositories.csv")
    repositories_df["Semantic Rating"] = None
    repositories_df["Syntactic Rating"] = None

    if not os.path.exists("rates.csv"):

        for index, row in repositories_df.iterrows():
            repo_url = row["Repository URL"]
            print("Evaluating repository: " + repo_url)


            repo_name = "/".join(repo_url.split("/")[-2:])

            syntactic_score = rate_repository_syntactic(repo_name, 'github')
            semantic_score = prompt_langchain(repo_url, 'rate')

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
            print('\n\n\n')
            # Save the updated DataFrame to a CSV
            repositories_df.to_csv("rates.csv", index=False)

    for index, row in repositories_df.iterrows():
        repo_url = row["Repository URL"]
        repo_name = "/".join(repo_url.split("/")[-2:])
        prompt_langchain(repo_url, 'improve')

        dir = "./improved_repos/" + repo_name
        syntactic_score = rate_repository_syntactic(repo_name, 'improved')
        semantic_score = prompt_langchain(dir, 'rate')
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

        print('\n\n\n')
        # Save the updated DataFrame to a CSV
        repositories_df.to_csv("rates_improved.csv", index=False)


