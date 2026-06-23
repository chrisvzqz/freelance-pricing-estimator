from playwright.sync_api import sync_playwright, Playwright
import json

def run (playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    
    projects_urls = []
    all_budgets = []

    for i in range(1, 51):
        page_urls, page_budgets = get_project_urls_from_listing_page(page, i)
        for url, bud in zip(page_urls, page_budgets):
            projects_urls.append(url)
            all_budgets.append(bud)

    extract_project_detail(page, projects_urls, all_budgets)
    
    browser.close()

def parse_budget(text):
    clean = text.replace(".", "").replace(",", "")

    if "hora" in text or "hour" in text:
        if "Más de" in text or "More than" in text:
            nums = [int(s) for s in clean.split() if s.isdigit()]
            return nums[0], None, "hourly"
        if "Menos de" in text or "Less than" in text:
            nums = [int(s) for s in clean.split() if s.isdigit()]
            return None, nums[0], "hourly"
        else:
            nums = [int(s) for s in clean.split() if s.isdigit()]
            return nums[0], nums[1], "hourly"
    
    elif "Más de" in text or "More than" in text:
        nums = [int(s) for s in clean.split() if s.isdigit()]
        return nums[0], None, "fixed_price"
    
    elif "Menos de" in text or "Less than" in text:
        nums = [int(s) for s in clean.split() if s.isdigit()]
        return None, nums[0], "fixed_price"

    else:
        nums = [int(s) for s in clean.split() if s.isdigit()]
        return nums[0], nums[1], "fixed_price"

def get_project_urls_from_listing_page(page, page_number):
    page.goto(f"https://www.workana.com/jobs?category=it-programming&language=es&page={page_number}")

    page.wait_for_selector(".project-item")
    proyectos = page.locator(".project-item").all()

    projects_urls = []
    budgets = []

    for proyecto in proyectos:
        url = proyecto.locator(".project-title a[href]").get_attribute("href")
        projects_urls.append(f"https://www.workana.com{url}")
        budgets.append(proyecto.locator("span.values span").text_content().strip())

    return projects_urls, budgets

def extract_project_detail(page, projects_urls, budgets):
    all_projects = []

    for i, url in enumerate(projects_urls):
        page.goto(url)
        page.wait_for_selector("section.project-view-v3")

        budget_raw = budgets[i]
        budget_min, budget_max, budget_type = parse_budget(budget_raw)

        skills_project = [
            s.get_attribute("title").replace("Trabajos Freelance de ", "")
            for s in page.locator(".skills a.skill").all()
        ]

        #mt20_fields = page.locator("article p.mt20:not(.specification):not(.bold) b").all()

        fields = page.evaluate("""
            () => {
                const p = document.querySelector('article p.mt20:not(.specification):not(.bold)');
                const result = {};
                const labels = Array.from(p.childNodes)
                    .filter(node => node.nodeType === 3 && node.textContent.trim() !== '')
                    .map(node => node.textContent.trim());
                const values = Array.from(p.querySelectorAll('b'))
                    .map(b => b.textContent.trim());
                labels.forEach((label, i) => result[label] = values[i]);
                return result;
            }
        """)

        project = {
            "title": page.locator("h1.title").text_content().strip(),
            "description": page.locator("div.expander").text_content().strip(),
            "budget_min": budget_min,
            "budget_max": budget_max,
            "budget_type": budget_type,
            "skills": skills_project,
            "category": fields.get("Categoría"),
            "subcategory": fields.get("Subcategoría"),
            "scope_project": fields.get("¿Cuál es el alcance del proyecto?"),
            "project_url": url,
            "platform": "Workana"
        }

        all_projects.append(project) 

    with open("data/raw/projects_workana.json", "w", encoding="utf-8") as f:
        json.dump(all_projects, f, indent=4, ensure_ascii=False)

with sync_playwright() as playwright:
    run(playwright)