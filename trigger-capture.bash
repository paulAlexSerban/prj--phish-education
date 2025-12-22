#!/bin/bash
source .env
# Script to trigger the singlefile-capture workflow using GitHub API

# Configuration
REPO_OWNER="paulAlexSerban"
REPO_NAME="prj--phish-education"
WORKFLOW_FILE="singlefile-capture.yml"
BRANCH="main"

# Check if GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN environment variable is not set"
  echo "Please set it with: export GITHUB_TOKEN='your-github-token'"
  exit 1
fi

# Parse command line arguments
URL=""
OUTPUT_FILENAME=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --url)
      URL="$2"
      shift 2
      ;;
    --output)
      OUTPUT_FILENAME="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 --url <URL> --output <OUTPUT_FILENAME>"
      echo ""
      echo "Options:"
      echo "  --url        URL of the webpage to capture (required)"
      echo "  --output     Output filename without extension (required)"
      echo ""
      echo "Example:"
      echo "  $0 --url https://example.com --output example-site"
      echo ""
      echo "Environment Variables:"
      echo "  GITHUB_TOKEN    Your GitHub personal access token (required)"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [ -z "$URL" ]; then
  echo "Error: --url is required"
  echo "Use --help for usage information"
  exit 1
fi

if [ -z "$OUTPUT_FILENAME" ]; then
  echo "Error: --output is required"
  echo "Use --help for usage information"
  exit 1
fi

# Trigger the workflow
echo "Triggering workflow..."
echo "  Repository: $REPO_OWNER/$REPO_NAME"
echo "  Workflow: $WORKFLOW_FILE"
echo "  URL: $URL"
echo "  Output: $OUTPUT_FILENAME"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/$WORKFLOW_FILE/dispatches \
  -d "{\"ref\":\"$BRANCH\",\"inputs\":{\"url\":\"$URL\",\"output_filename\":\"$OUTPUT_FILENAME\"}}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 204 ]; then
  echo "✓ Workflow triggered successfully!"
  echo ""
  echo "View workflow runs at:"
  echo "https://github.com/$REPO_OWNER/$REPO_NAME/actions"
else
  echo "✗ Failed to trigger workflow"
  echo "HTTP Status: $HTTP_CODE"
  echo "Response: $BODY"
  exit 1
fi
