import json
import sys

index_file = sys.argv[1]
year = int(sys.argv[2])
url = sys.argv[3]
domain = sys.argv[4]
filename = sys.argv[5]
timestamp = sys.argv[6]

# Read existing data
with open(index_file, 'r') as f:
    data = json.load(f)

# Remove placeholder if it exists
data = [item for item in data if item.get('year') != 0]

# Create new entry
new_entry = {
    "year": year,
    "url": url,
    "domain": domain,
    "filename": filename,
    "description": f"Phishing page captured from {domain}",
    "capturedAt": timestamp,
    "path": f"{year}/{filename}/index.html"
}

# Add new entry
data.append(new_entry)

# Sort by year and timestamp (newest first)
data.sort(key=lambda x: (x.get('year', 0), x.get('capturedAt', '')), reverse=True)

# Write updated data
with open(index_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Added entry for {domain} to index.json")