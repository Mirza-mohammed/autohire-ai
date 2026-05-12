from app.core.celery_app import celery_app
from playwright.sync_api import sync_playwright
import time
import random
import os

def random_delay(min_ms=500, max_ms=1500):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

@celery_app.task
def auto_apply_task(job_url: str, user_profile_data: dict, resume_pdf_path: str):
    """
    Background task to automatically apply to a job using Playwright.
    """
    print(f"[Auto-Apply] Starting auto-apply for {job_url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(job_url, wait_until="networkidle")
            random_delay()
            
            # Simple heuristic mapping for Lever forms
            if "lever.co" in job_url:
                print("[Auto-Apply] Detected Lever form")
                
                # Fill basic info
                first_name = user_profile_data.get("first_name", "Test")
                last_name = user_profile_data.get("last_name", "User")
                email = user_profile_data.get("email", "test@example.com")
                
                page.fill("input[name='name']", f"{first_name} {last_name}")
                random_delay()
                page.fill("input[name='email']", email)
                random_delay()
                
                # Upload Resume
                if os.path.exists(resume_pdf_path):
                    page.set_input_files("input[type='file'][name='resume']", resume_pdf_path)
                    print("[Auto-Apply] Uploaded Resume")
                
                random_delay()
                
                # We do NOT click submit in development to avoid spamming real companies.
                # page.click("button[type='submit']")
                print("[Auto-Apply] Filled form. Skipping submit for safety.")
                
            elif "greenhouse.io" in job_url:
                print("[Auto-Apply] Detected Greenhouse form")
                # Add Greenhouse logic here...
                pass
            
            return {"status": "success", "url": job_url}
            
        except Exception as e:
            print(f"[Auto-Apply Error] {e}")
            # Take screenshot on failure for debugging
            page.screenshot(path="apply_failure.png")
            return {"status": "failed", "error": str(e)}
        finally:
            browser.close()
