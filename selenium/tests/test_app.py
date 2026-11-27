from pathlib import Path

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

import app

DESCRIPTION = "A test page description"
HTTPS_URL = "https://example.com/"


@pytest.fixture
def chrome(monkeypatch):
    instances = []

    class FakeChrome:
        constructor_error = None
        navigation_error = None
        find_error = None
        quit_error = None

        def __init__(self, *, service, options):
            (profile,) = (
                Path(argument.removeprefix("--user-data-dir="))
                for argument in options.arguments
                if argument.startswith("--user-data-dir=")
            )
            self.profile = profile
            self.calls = []
            instances.append(self)
            assert profile.parent == Path("/tmp")
            assert profile.is_dir()
            if self.constructor_error:
                raise self.constructor_error

        def set_page_load_timeout(self, seconds):
            self.calls.append(("set_page_load_timeout", seconds))

        def get(self, url):
            assert self.profile.is_dir()
            self.calls.append(("get", url))
            if self.navigation_error:
                raise self.navigation_error

        def find_element(self, by, selector):
            self.calls.append(("find_element", by, selector))
            if self.find_error:
                raise self.find_error
            return self

        def get_attribute(self, name):
            self.calls.append(("get_attribute", name))
            return DESCRIPTION

        def quit(self):
            assert self.profile.is_dir()
            self.calls.append(("quit",))
            if self.quit_error:
                raise self.quit_error

    monkeypatch.setattr(app.webdriver, "Chrome", FakeChrome)
    return FakeChrome, instances


@pytest.mark.parametrize("url", [HTTPS_URL, "data:text/html,<title>Test</title>"])
def test_handler_returns_description(chrome, url):
    _, instances = chrome

    assert app.handler({"url": url}) == {"url": url, "description": DESCRIPTION}

    (driver,) = instances
    assert driver.calls == [
        ("set_page_load_timeout", app.PAGE_LOAD_TIMEOUT_SECONDS),
        ("get", url),
        ("find_element", By.CSS_SELECTOR, 'meta[name="description"]'),
        ("get_attribute", "content"),
        ("quit",),
    ]
    assert not driver.profile.exists()


@pytest.mark.parametrize(
    "event",
    [
        {},
        [],
        None,
        {"url": 123},
        {"url": "ftp://example.com/"},
        {"url": "file:///etc/passwd"},
        {"url": "https:///nohost"},
        {"url": "http://:80"},
    ],
)
def test_handler_rejects_invalid_event_before_starting_chrome(chrome, event):
    _, instances = chrome

    with pytest.raises(ValueError):
        app.handler(event)

    assert instances == []


@pytest.mark.parametrize(
    ("error_attribute", "error"),
    [
        ("navigation_error", TimeoutException("navigation timed out")),
        ("find_error", NoSuchElementException("description is missing")),
    ],
)
def test_handler_closes_chrome_and_removes_profile_on_page_error(
    chrome, error_attribute, error
):
    fake, instances = chrome
    setattr(fake, error_attribute, error)

    with pytest.raises(type(error)) as raised:
        app.handler({"url": HTTPS_URL})

    assert raised.value is error
    (driver,) = instances
    assert driver.calls.count(("quit",)) == 1
    assert not driver.profile.exists()


def test_handler_preserves_result_when_quit_fails(chrome, capsys):
    fake, instances = chrome
    fake.quit_error = RuntimeError("Chrome quit failed")

    assert app.handler({"url": HTTPS_URL}) == {
        "url": HTTPS_URL,
        "description": DESCRIPTION,
    }

    (driver,) = instances
    assert driver.calls.count(("quit",)) == 1
    assert "chrome.quit() failed" in capsys.readouterr().out
    assert not driver.profile.exists()


def test_handler_removes_profile_when_chrome_constructor_fails(chrome):
    fake, instances = chrome
    error = RuntimeError("Chrome failed to start")
    fake.constructor_error = error

    with pytest.raises(RuntimeError) as raised:
        app.handler({"url": HTTPS_URL})

    assert raised.value is error
    (driver,) = instances
    assert not driver.profile.exists()


def test_handler_uses_a_new_profile_per_invocation(chrome):
    _, instances = chrome

    app.handler({"url": HTTPS_URL})
    app.handler({"url": HTTPS_URL})

    first, second = instances
    assert first.profile != second.profile
    assert not first.profile.exists()
    assert not second.profile.exists()
