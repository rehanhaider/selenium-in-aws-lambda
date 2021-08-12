#!/usr/bin/bash

declare -A chrome_versions

# Enter the list of browsers to be downloaded
### Using Chromium as documented here - https://www.chromium.org/getting-involved/download-chromium
chrome_versions=( ['89.0.4389.47']='843831' )
chrome_drivers=( "89.0.4389.23" )
#firefox_versions=( "86.0" "87.0b3" )
#gecko_drivers=( "0.29.0" )

# Download Chrome
for br in "${!chrome_versions[@]}"
do
    echo "Downloading Chrome version $br"
    mkdir -p "/opt/chrome/stable"
    curl -Lo "/opt/chrome/stable/chrome-linux.zip" \
    "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F${chrome_versions[$br]}%2Fchrome-linux.zip?alt=media"
    unzip -q "/opt/chrome/stable/chrome-linux.zip" -d "/opt/chrome/stable/"
    mv /opt/chrome/stable/chrome-linux/* /opt/chrome/stable/
    rm -rf /opt/chrome/stable/chrome-linux "/opt/chrome/stable/chrome-linux.zip"
done

# Download Chromedriver
for dr in ${chrome_drivers[@]}
do
    echo "Downloading Chromedriver version $dr"
    mkdir -p "/opt/chromedriver/stable/"
    curl -Lo "/opt/chromedriver/stable//chromedriver_linux64.zip" \
    "https://chromedriver.storage.googleapis.com/$dr/chromedriver_linux64.zip"
    unzip -q "/opt/chromedriver/stable//chromedriver_linux64.zip" -d "/opt/chromedriver/stable/"
    chmod +x "/opt/chromedriver/stable/chromedriver"
    rm -rf "/opt/chromedriver/stable/chromedriver_linux64.zip"
done

echo "Chrome & Chromedriver installed"