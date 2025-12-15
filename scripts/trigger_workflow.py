import requests

token = "YOUR_GITHUB_TOKEN"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

data = {
    "ref": "main",
    "inputs": {
        "url": "https://example.com",
        "output_filename": "example-site"
    }
}

response = requests.post(
    "https://api.github.com/repos/Hackout-ro/phishing-catalogue-automation-PoC/actions/workflows/singlefile-capture.yml/dispatches",
    headers=headers,
    json=data
)

print(f"Status: {response.status_code}")