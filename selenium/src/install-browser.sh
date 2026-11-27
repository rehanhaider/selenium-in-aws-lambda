#!/bin/bash
set -euo pipefail

download_urls=$(
    curl -fsSL https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json |
        python3 -c '
import json
import sys

version = sys.argv[1]
manifest = json.load(sys.stdin)
release = next((entry for entry in manifest["versions"] if entry["version"] == version), None)
if release is None:
    sys.exit(f"Chrome for Testing version {version} was not found")

urls = []
for artifact in ("chrome-headless-shell", "chromedriver"):
    downloads = release["downloads"].get(artifact, [])
    url = next((item["url"] for item in downloads if item["platform"] == "linux64"), None)
    if url is None:
        sys.exit(f"Chrome for Testing version {version} has no linux64 download for {artifact}")
    urls.append(url)
print(*urls)
' "${1:?Pass CHROME_VERSION as the first argument}"
)
read -r shell_url driver_url <<< "$download_urls"

curl -fsSL "$shell_url" -o /tmp/chrome-headless-shell.zip
unzip -q /tmp/chrome-headless-shell.zip -d /tmp/
mv /tmp/chrome-headless-shell-linux64 /opt/chrome-headless-shell

curl -fsSL "$driver_url" -o /tmp/chromedriver.zip
unzip -q /tmp/chromedriver.zip -d /tmp/
mv /tmp/chromedriver-linux64/chromedriver /opt/chromedriver
