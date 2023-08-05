import requests

query = "size:<30 language:Python"  # Search for Python repositories with less than 30KB of code.
sort = "stars"  # Sort results by number of stars.
order = "desc"  # Sort in descending order.
url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}"

headers = {"Authorization": "token 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"}
response = requests.get(url, headers=headers)

# Print the full names of the repositories.
for repo in response.json()["items"]:
    print(repo["full_name"])
