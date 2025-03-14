import os
import requests
import json
from github import Github

# GitHub API Authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama API endpoint

def get_pr_diff():
    """Fetch PR code changes from GitHub."""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    response = requests.get(url, headers=HEADERS)
    files = response.json()
    return files

def analyze_code_with_llama(code):
    """Send code snippet to Llama 3.2 for AI review."""
    payload = {
        "model": "llama3.2",
        "prompt": f"Review this code for best practices, security, and efficiency:\n{code}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()
    return result["response"]

def post_review_comment(filename, line, comment):
    """Post AI-generated review comment on GitHub."""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/comments"
    payload = {
        "body": comment,
        "path": filename,
        "position": line
    }
    requests.post(url, headers=HEADERS, json=payload)
    #Comment
if __name__ == "__main__":
    files = get_pr_diff()
    for file in files:
        filename = file["filename"]
        patch = file.get("patch", "")
        if patch:
            ai_review = analyze_code_with_llama(patch)
            post_review_comment(filename, 1, ai_review)
