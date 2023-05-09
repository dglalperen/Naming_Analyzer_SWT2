from github import Github
import operator

GITHUB_TOKEN = "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"

def get_most_used_language(repo_url):
    # Initialize a Github instance with your access token
    g = Github(GITHUB_TOKEN)

    # Extract user and repo name from the URL
    try:
        user, repo_name = repo_url.split("github.com/")[1].split("/", 1)
    except IndexError:
        return "Invalid GitHub repository URL."

    repo_name = repo_name.rstrip("/")

    # Get the repository and languages
    try:
        repo = g.get_repo(f"{user}/{repo_name}")
        languages = repo.get_languages()
    except Exception as e:
        return f"Error: {str(e)}"

    if not languages:
        return "No languages detected in the repository."

    # Find the most used language
    most_used_language = max(languages.items(), key=operator.itemgetter(1))[0]

    return most_used_language
