import os
import time
import urllib.request

import pytest
from playwright.sync_api import sync_playwright


def _wait_for_health(base_url: str, timeout_s: int = 30) -> None:
    deadline = time.time() + timeout_s
    url = base_url.rstrip("/") + "/api/health"
    last_err = None

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return
        except Exception as e:
            last_err = e
            time.sleep(0.5)

    raise RuntimeError(f"App did not become ready at {url}: {last_err}")


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ["BASE_URL"]


@pytest.fixture(scope="session", autouse=True)
def wait_for_app(base_url: str):
    _wait_for_health(base_url)
    yield


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-web-security",
            ],
        )
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
