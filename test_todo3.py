# playwright codegen demo.playwright.dev/todomvc/#/
import time
from playwright.sync_api import Playwright


def test_add_todo(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill(
        "Создать первый сценарий playwright"
    )
    page.get_by_placeholder("What needs to be done?").press("Enter")
    page.get_by_role("checkbox", name="Toggle Todo").check()
    time.sleep(3)
    # ---------------------

    context.close()
    browser.close()
