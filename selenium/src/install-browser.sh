#!/bin/bash


echo "Downloading Chromium..."
curl "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F$CHROMIUM_VERSION%2Fchrome-linux.zip?generation=1652397748160413&alt=media" > /tmp/chromium.zip

unzip /tmp/chromium.zip -d /tmp/
mv /tmp/chrome-linux/ /opt/chrome

echo "Chromium version"
/opt/chrome/chrome --version

curl "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F$CHROMIUM_VERSION%2Fchromedriver_linux64.zip?generation=1652397753719852&alt=media" > /tmp/chromedriver_linux64.zip
unzip /tmp/chromedriver_linux64.zip -d /tmp/
mv /tmp/chromedriver_linux64/chromedriver /opt/chromedriver
