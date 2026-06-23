from playwright.sync_api import sync_playwright, Playwright
import json

def run (playwright: Playwright):
    chronium = playwright.chromium
    browser = chronium.launch(headless=False)
    page = browser.new_page()

    # ...

    browser.close()

with sync_playwright() as playwright:
    run(playwright)