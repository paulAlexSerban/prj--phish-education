# Phish Education - Phishing Webpage Capture Automation

This repository contains a proof of concept for automating the capture and cataloging of phishing webpages using the SingleFile browser extension's CLI tool. The automation is implemented using GitHub Actions to streamline the process of capturing webpages and storing them in a structured manner.

## Triggering the Workflow Locally

```bash
bash trigger-workflow.sh --url PHISHING_URL --output OUTPUT_FILENAME
```

Replace `PHISHING_URL` with the URL of the phishing webpage you want to capture and `OUTPUT_FILENAME` with the desired name for the output file.

---

1. **Create a new GitHub Personal Access Token** with the correct permissions:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name it: `Workflow Trigger`
   - **Select these scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
   - Click "Generate token"
   - Copy the token

2. **Update your .env file**:
   ```bash
   GITHUB_TOKEN=your_new_token_here
   ```

3. **Run the script again**:
   ```bash
   bash ./trigger-capture.bash --url https://example.com --output examplesite
   ```
