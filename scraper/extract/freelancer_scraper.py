from playwright.sync_api import sync_playwright, Playwright
import json

def run (playwright: Playwright):
    chronium = playwright.chromium
    browser = chronium.launch(headless=False)
    page = browser.new_page()

    urls = extract_jobs_urls(page)

    url_job = []

    for url in urls:
        page.goto(f"https://www.freelancer.com{url}")

        page.wait_for_selector("#project-list")

        jobs = page.locator(".JobSearchCard-item").all()

        for job in jobs:
            url_prjct = job.locator("a.JobSearchCard-primary-heading-link").get_attribute("href")
            if url_prjct.startswith("/projects"):
                url_job.append(url_prjct)
        break

    for url_j in url_job:
        page.goto(f"https://www.freelancer.com{url_j}")
        

    browser.close()

def extract_jobs_urls(page):
    page.goto("https://www.freelancer.com/job/")

    page.wait_for_selector(".PageJob")

    job_list = []

    secciones = page.locator("section.PageJob-category").all()
    
    for sec in secciones:
        categoria = sec.locator("h3").text_content().strip()
        if categoria.startswith("Websites, IT & Software") or categoria.startswith("Artificial Intelligence"):
            areas = sec.locator("ul li a").all()
            for a in areas:
                text = a.text_content().strip()
                num = int(text.split("(")[-1].replace(")", ""))
                if num > 0 and a.get_attribute("href").startswith("/jobs"):
                    job_list.append(a.get_attribute("href"))

    return job_list

with sync_playwright() as playwright:
    run(playwright)