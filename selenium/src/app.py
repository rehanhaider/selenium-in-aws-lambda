# Use Selenium and ChromeDriver to read a page's meta description.
import resource
import shutil
import tempfile
from urllib.parse import urlsplit

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Keep below the function's 120 s timeout, so a slow navigation raises
# TimeoutException and fails the invocation instead of Lambda killing it.
PAGE_LOAD_TIMEOUT_SECONDS = 90

# With --single-process, Chrome segfaults while shutting down, after the page
# work is done. Each crash would write a ~95 MB core file to /tmp, filling a
# warm container's /tmp and memory. Chrome inherits this limit.
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def handler(event=None, context=None):
    if not isinstance(event, dict):
        raise ValueError("event must be a dict")
    if "url" not in event:
        raise ValueError("event must contain 'url'")
    url = event["url"]
    if not isinstance(url, str):
        raise ValueError("url must be a string")

    parsed_url = urlsplit(url)
    scheme = parsed_url.scheme.lower()
    if scheme not in ("http", "https", "data"):
        raise ValueError("url scheme must be http, https, or data")
    if scheme in ("http", "https") and not parsed_url.hostname:
        raise ValueError("http and https URLs must include a host")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome-headless-shell/chrome-headless-shell"
    # Tells chromedriver the binary is chrome-headless-shell, which it launches
    # differently from full Chrome. Without it, session creation fails.
    chrome_options.set_capability("browserName", "chrome-headless-shell")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("window-size=2560x1440")
    # A fresh profile per invocation, so cookies and storage from one caller's
    # page do not carry into the next invocation in a warm container.
    user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-", dir="/tmp")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--remote-debugging-port=9222")
    #chrome_options.add_argument("--data-path=/tmp/chrome-user-data")
    #chrome_options.add_argument("--disk-cache-dir=/tmp/chrome-user-data")
    try:
        chrome = webdriver.Chrome(service=Service("/opt/chromedriver"), options=chrome_options)
        try:
            chrome.set_page_load_timeout(PAGE_LOAD_TIMEOUT_SECONDS)
            chrome.get(url)
            description = chrome.find_element(
                By.CSS_SELECTOR, 'meta[name="description"]'
            ).get_attribute("content")
        finally:
            try:
                chrome.quit()
            except Exception as exc:
                # A failed cleanup must not replace the scrape's result or its error.
                print(f"chrome.quit() failed: {exc!r}")
    finally:
        shutil.rmtree(user_data_dir, ignore_errors=True)
    return {"url": url, "description": description}
