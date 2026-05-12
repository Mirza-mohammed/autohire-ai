from app.core.celery_app import celery_app
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import random

def random_delay(min_ms=1000, max_ms=3000):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

@celery_app.task
def scrape_job_board_task(company_careers_url: str):
    """
    Background task to scrape a company's job board (e.g., Lever/Greenhouse) using Playwright.
    """
    print(f"[Scraper Task] Starting scrape for {company_careers_url}")
    
    with sync_playwright() as p:
        # For production, we use proxies and specific user agents
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(company_careers_url, wait_until="networkidle")
            random_delay()
            
            # Use BeautifulSoup to parse the complex DOM easily
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            jobs = []
            
            # Simple heuristic for common Lever/Greenhouse boards
            # Lever: div.posting
            # Greenhouse: div.opening
            postings = soup.find_all('div', class_=['posting', 'opening', 'job-posting'])
            
            for post in postings:
                title_elem = post.find('h5') or post.find('a')
                if title_elem:
                    title = title_elem.text.strip()
                    link = title_elem.get('href') if title_elem.name == 'a' else post.find('a').get('href')
                    if link and link.startswith('/'):
                        # Very naive relative URL resolution
                        from urllib.parse import urlparse
                        parsed_url = urlparse(company_careers_url)
                        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                        link = base_url + link
                    
                    jobs.append({"title": title, "url": link})
            
            print(f"[Scraper Task] Found {len(jobs)} jobs.")
            
            # TODO: In the next step, we will pass these URLs to the Agent Evaluator
            # to see if any match the user's profile.
            
            return jobs
            
        except Exception as e:
            print(f"[Scraper Task Error] {e}")
            return {"error": str(e)}
        finally:
            browser.close()
