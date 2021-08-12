from selenium import webdriver


def handler(event=None, context=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/stable/chrome"
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
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome = webdriver.Chrome("/opt/chromedriver/stable/chromedriver", options=chrome_options)
    chrome.get("https://cloudbytes.dev")
    return chrome.find_element_by_xpath("//html").text