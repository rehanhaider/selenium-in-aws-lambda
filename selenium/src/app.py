## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
import json
import os.path
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



def handler(event=None, context=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("window-size=2560x1440")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9222")
    #chrome_options.add_argument("--data-path=/tmp/chrome-user-data")
    #chrome_options.add_argument("--disk-cache-dir=/tmp/chrome-user-data")
    chrome = webdriver.Chrome("/opt/chromedriver", options=chrome_options)
    chrome.get("https://cloudbytes.dev/")
    description = chrome.find_element(By.NAME, "description").get_attribute("content")
    print(description)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": description,
            }
        ),
    }
