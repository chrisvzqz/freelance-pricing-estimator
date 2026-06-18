from playwright.sync_api import sync_playwright, Playwright

def run (playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    num = 11
    for n in range(1, num):
        page.goto(f"https://www.workana.com/jobs?category=it-programming&language=es&page={n}")
        
        page.wait_for_selector(".project-item")
        proyectos = page.locator(".project-item").all()

        for proyecto in proyectos:
            titulo = proyecto.locator(".project-title span[title]").get_attribute("title")
            print(titulo)
        


    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)