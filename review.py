import os
import requests
import json
from github import Github

# GitHub API Authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

print(f"Using Repository: {REPO}")  # Debugging
print(f"Pull Request Number: {PR_NUMBER}")  # Debugging

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama API endpoint

def get_pr_diff():
    """Fetch PR code changes from GitHub."""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    response = requests.get(url, headers=HEADERS)

    try:
        files = response.json()  # Ensure it's parsed as JSON
    except json.JSONDecodeError:
        print("Error: Failed to parse GitHub API response.")
        print("Response:", response.text)  # Debugging info
        return []

    if not isinstance(files, list):
        print("Error: GitHub API response is not a list.")
        print("Response:", files)
        return []

    return files

def analyze_code_with_llama(code):
    """Send code snippet to Llama 3.2 for AI review."""
    payload = {
        "model": "llama3.2",
        "prompt": f"Review this code and give a final score for best practices, security, and efficiency:\n{code} ",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()
    print(result)  # Debugging
    return result.get("response", "No response from AI.")

def post_review_comment(filename, line, comment):
    """Post AI-generated review comment on GitHub."""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/comments"
    payload = {
        "body": comment,
        "path": filename,
        "position": line
    }
    requests.post(url, headers=HEADERS, json=payload)

if __name__ == "__main__":
    files = get_pr_diff()
    
    if not files:
        print("No files changed in this PR or failed to fetch PR data.")
    else:
        for file in files:
            if isinstance(file, dict) and "filename" in file:
                filename = file["filename"]
                patch = file.get("patch", "")
                if patch:
                    ai_review = analyze_code_with_llama(patch)
                    post_review_comment(filename, 1, ai_review)
            else:
                print("Error: Unexpected response format from GitHub API:", file)

