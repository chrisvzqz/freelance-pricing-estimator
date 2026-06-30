from playwright.sync_api import sync_playwright, Playwright
import json
import re

def run (playwright: Playwright):
    chronium = playwright.chromium
    browser = chronium.launch(headless=False)
    page = browser.new_page()

    urls = extract_jobs_urls(page)
    # En flujo normal se tendrian que obtener de aqui las urls, pero al haber guardado un .txt pues las cogemos de ahí
    urls_prjcts = get_urls_all_projects(page, urls) 

    with open("data/raw/url_projects_freelancer.json", "w", encoding="utf-8") as f:
        json.dump(urls_prjcts, f, indent=4, ensure_ascii=False)

    all_projects = []

    for i, item in enumerate(urls_prjcts):
        url = item["href"]
        categoria = item["categoria"]
        
        page.goto(url)

        page.wait_for_selector(".ContentContainer")

        budget_min, budget_max, currency, budget_type = parse_budget(page.locator("h2.text-body-24").text_content().strip())

        skills_project = [sk.text_content().strip() for sk in page.locator("fl-link.Tag .Content").all()]

        project = {
            'title': page.locator("h1.text-body-24").text_content().strip(),
            'description': page.locator(".Project-description").text_content().strip(),
            'budget_min': budget_min,
            'budget_max': budget_max,
            'currency': currency,
            'budget_type': budget_type,
            'skills': skills_project,
            'project_url': url,
            'category': categoria,
            'subcategory': page.locator('fl-breadcrumbs-item[fltrackinglabel="ProjectViewLoggedOut-BreadcrumbSkill"] span').text_content().strip(),
            'platform': "Freelancer"
        }
        
        all_projects.append(project)
        
        # if i == 10:
        #     break

    with open("data/raw/projects_freelancer.json", "w", encoding="utf-8") as f:
        json.dump(all_projects, f, indent=4, ensure_ascii=False)

    browser.close()

def parse_budget(text):
    if not text:
        return None, None, None, None

    budget_type = "hourly" if "hour" in text.lower() else "fixed_price"

    currency_map = {
        "$": "USD",
        "€": "EUR",
        "£": "GBP",
        "₹": "INR",
        "CAD": "CAD",
        "AUD": "AUD"
    }
    currency = None
    for symbol, code in currency_map.items():
        if symbol in text:
            currency = code
            break

    nums = re.findall(r"[\d,]+(?:\.\d+)?", text)
    nums = [int(float(n.replace(",", ""))) for n in nums]

    if len(nums) == 2:
        budget_min, budget_max = nums[0], nums[1]
    elif len(nums) == 1:
        budget_min, budget_max = nums[0], None
    else:
        budget_min, budget_max = None, None

    return budget_min, budget_max, currency, budget_type

def get_urls_all_projects(page, urls):
    url_job = []

    for item in urls:
        url = item["href"]
        categoria = item["categoria"]

        try:
            page.goto(f"https://www.freelancer.com{url}")
            page.wait_for_load_state("networkidle")
            page.wait_for_selector("#project-list", state="visible", timeout=15000)
        except Exception as e:
            print(f"⚠️ Saltando categoría {url} por error: {e}")
            continue

        href = page.locator("li[data-link='last_page'] a").first.get_attribute("href")

        url_base, num_pags_str = href.rsplit("/", 1)
        
        if num_pags_str.isdigit():
            num_pags = int(num_pags_str)
        else:
            url_base = href
            num_pags = 1

        for pag in range(1, num_pags + 1):
            if num_pags == 1:
                target_url = url_base
            else:
                target_url = f"{url_base}/{pag}"

            try:
                page.goto(target_url)
                page.wait_for_load_state("networkidle")
                page.wait_for_selector("#project-list", state="visible", timeout=15000)
            except Exception as e:
                print(f"⚠️ Saltando página {target_url} por error: {e}")
                continue

            jobs = page.locator(".JobSearchCard-item").all()
            for job in jobs:
                url_prjct = job.locator("a.JobSearchCard-primary-heading-link").get_attribute("href")
                if url_prjct.startswith("/projects"):
                    url_job.append({
                        "url": f"https://www.freelancer.com{url_prjct}",
                        "categoria": categoria
                    })

    return url_job  


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
                excluir = ["AI Translation", "AI-Generated Art", "Voice Synthesis"]
                if num > 0 and a.get_attribute("href").startswith("/jobs") and not any(text.startswith(e) for e in excluir):
                    job_list.append({
                        "href": a.get_attribute("href"),
                        "categoria": categoria.split("(")[0].strip()
                    })

    return job_list

with sync_playwright() as playwright:
    run(playwright)