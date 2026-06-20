from playwright.sync_api import sync_playwright, Playwright
import json

def run (playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://www.workana.com/jobs?category=it-programming&language=es&page=1")
    
    page.wait_for_selector(".project-item")
    proyectos = page.locator(".project-item").all()

    urls = []
    budgets = []

    for proyecto in proyectos:
        href = proyecto.locator(".project-title a[href]").get_attribute("href")
        urls.append(f"https://www.workana.com{href}")
        budgets.append(proyecto.locator("span.values span").text_content().strip())

    all_projects = []

    for i, url in enumerate(urls):
        page.goto(url)
        page.wait_for_selector("section.project-view-v3")

        budget_raw = budgets[i]
        budget_min, budget_max, budget_type = parse_budget(budget_raw)

        skills_project = [
            s.get_attribute("title").replace("Trabajos Freelance de ", "")
            for s in page.locator(".skills a.skill").all()
        ]

        mt20_fields = page.locator("article p.mt20:not(.specification):not(.bold) b").all()

        project = {
            "title": page.locator("h1.title").text_content().strip(),
            "description": page.locator("div.expander").text_content().strip(),
            "budget_min": budget_min,
            "budget_max": budget_max,
            "budget_type": budget_type,
            "skills": skills_project,
            "category": mt20_fields[0].text_content().strip(),
            "subcategory": mt20_fields[1].text_content().strip(),
            "scope_project": mt20_fields[2].text_content().strip(), # Revisar
            "project_url": url,
            "platform": "Workana"
        }

        all_projects.append(project) 

    with open("data/raw/projects.json", "w", encoding="utf-8") as f:
        json.dump(all_projects, f, indent=4, ensure_ascii=False)
    
    # other actions...
    browser.close()

def parse_budget(text):
    clean = text.replace(".", "").replace(",", "")

    if "hora" in text or "hour" in text:
        nums = [int(s) for s in clean.split() if s.isdigit()]
        return nums[0], nums[1], "hourly"
    
    elif "Más de" in text or "More than" in text:
        nums = [int(s) for s in clean.split() if s.isdigit()]
        return nums[0], None, "fixed_price"
    
    else:
        nums = [int(s) for s in clean.split() if s.isdigit()]
        return nums[0], nums[1], "fixed_price"

def get_project_urls_from_listing_page(page, page_number):
    page.goto(f"https://www.workana.com/jobs?category=it-programming&language=es&page={page_number}")

    page.wait_for_selector(".project-item")
    proyectos = page.locator(".project-item").all()

    for proyecto in proyectos:
        url = proyecto.locator(".project-title a[href]").get_attribute("href")
        project_urls = f"https://www.workana.com{url}"

    return project_urls

def extract_project_detail(project_urls):
    return

with sync_playwright() as playwright:
    run(playwright)