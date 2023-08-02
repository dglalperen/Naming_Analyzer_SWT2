
from rate_repository import rate_repository_sematic
from repos import check_github_api_credentials
from syntactic_score import rate_repository_syntactic
from repos import clone_repo, delete_repo

if __name__ == "__main__":
    GITHUB_API_URL = "https://api.github.com"
    github_token = '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'
    repo_url = 'https://github.com/vfaronov/httpolice'
    gpt4_key = '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'
    gpt3_key = "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"


    if(check_github_api_credentials(GITHUB_API_URL, github_token)):

        python_files = clone_repo(repo_url, github_token)
        repo_name = "/".join(repo_url.split("/")[-2:])

        syntactic_score = rate_repository_syntactic(repo_name)
        print(syntactic_score)

        semantic_score = rate_repository_sematic(python_files, gpt4_key)
        print(semantic_score)

        # delete repository
        delete_repo(repo_url)


    else:
        print("Github API credentials are not valid")




# Bewertung in GPT 4
# Verbesserung in GPT 3.5
