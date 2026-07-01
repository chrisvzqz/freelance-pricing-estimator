from playwright.sync_api import sync_playwright, Playwright
import json
import re

def run (playwright: Playwright):
    chronium = playwright.chromium
    browser = chronium.launch(headless=False)
    page = browser.new_page()

    urls = extract_jobs_urls(page)
    extract_projects_data(page, urls)

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

def extract_projects_data(page, urls, output_path="data/raw/projects_freelancer.jsonl"):
    
    # Cargar URLs ya procesadas para no repetir
    processed_urls = set() # con set para evitar duplicados
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            for line in f:
                project = json.loads(line)
                processed_urls.add(project["project_url"]) # Coge solo la url del proyecto y lo mete en el set
    except FileNotFoundError:
        pass

    for item in urls:
        url = item["href"]
        categoria = item["categoria"]

        try:
            page.goto(f"https://www.freelancer.com{url}")
            page.wait_for_load_state("networkidle")
            page.wait_for_selector("#project-list", state="visible", timeout=15000)
        except Exception as e:
            print(f"⚠️ Saltando categoría {url}: {e}")
            continue

        href = page.locator("li[data-link='last_page'] a").first.get_attribute("href")
        url_base, num_pags_str = href.rsplit("/", 1)
        if num_pags_str.isdigit():
            num_pags = int(num_pags_str)
        else:
            url_base = href
            num_pags = 1

        for pag in range(1, num_pags + 1):
            target_url = url_base if num_pags == 1 else f"{url_base}/{pag}"

            try:
                page.goto(target_url)
                page.wait_for_load_state("networkidle")
                page.wait_for_selector("#project-list", state="visible", timeout=15000)
            except Exception as e:
                print(f"⚠️ Saltando página {target_url}: {e}")
                continue

            jobs = page.locator(".JobSearchCard-item").all()
            for job in jobs:
                url_prjct = job.locator("a.JobSearchCard-primary-heading-link").get_attribute("href")
                if not url_prjct.startswith("/projects"):
                    continue
                
                full_url = f"https://www.freelancer.com{url_prjct}"
                
                # Saltar si ya fue procesado
                if full_url in processed_urls:
                    print(f"⏭️ Ya procesado: {full_url}")
                    continue

                try:
                    page.goto(full_url)
                    page.wait_for_selector(".ContentContainer", timeout=15000)
                    budget_min, budget_max, currency, budget_type = parse_budget(
                        page.locator("h2.text-body-24").text_content().strip()
                    )
                    skills_project = [sk.text_content().strip() for sk in page.locator("fl-link.Tag .Content").all()]
                    project = {
                        'title': page.locator("h1.text-body-24").text_content().strip(),
                        'description': page.locator(".Project-description").text_content().strip(),
                        'budget_min': budget_min,
                        'budget_max': budget_max,
                        'currency': currency,
                        'budget_type': budget_type,
                        'skills': skills_project,
                        'project_url': full_url,
                        'category': categoria,
                        'subcategory': page.locator('fl-breadcrumbs-item[fltrackinglabel="ProjectViewLoggedOut-BreadcrumbSkill"] span').text_content().strip(),
                        'platform': "Freelancer"
                    }
                    with open(output_path, "a", encoding="utf-8") as f:
                        json.dump(project, f, ensure_ascii=False)
                        f.write("\n")
                    processed_urls.add(full_url)

                except Exception as e:
                    print(f"⚠️ Error scrapeando proyecto {full_url}: {e}")
                    continue  


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