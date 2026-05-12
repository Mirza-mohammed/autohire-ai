from app.core.celery_app import celery_app
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import random
import os
from app.automation.session_manager import SessionManager
from app.automation.dynamic_selectors import dynamic_selector
from app.services.pdf_generator import PDFGeneratorService

def random_delay(min_ms=1000, max_ms=2500):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

@celery_app.task
def auto_apply_task(job_url: str, user_profile_data: dict, tailored_resume_data: dict = None):
    """
    Background task to automatically apply to a job using Playwright.
    Generates a dynamic PDF resume before applying.
    """
    print(f"[Auto-Apply] Starting auto-apply for {job_url}")
    
    # Generate the dynamic PDF
    pdf_service = PDFGeneratorService()
    if not tailored_resume_data:
        # Mock data if not provided by the pipeline
        tailored_resume_data = {
            "skills_to_highlight": ["Python", "Playwright", "Docker"],
            "tailored_experience": [{"title": "Software Engineer", "company": "Tech Corp", "tailored_bullets": ["Built AI agents"]}]
        }
    
    name = user_profile_data.get("first_name", "Test") + " " + user_profile_data.get("last_name", "User")
    email = user_profile_data.get("email", "test@example.com")
    resume_pdf_path = pdf_service.generate_ats_pdf(tailored_resume_data, name, email)
    print(f"[Auto-Apply] Generated dynamic ATS PDF at: {resume_pdf_path}")

    session_mgr = SessionManager()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Determine platform to load correct session
        platform = "handshake" if "handshake" in job_url.lower() else "generic"
        context = session_mgr.load_context(browser, platform)
        
        page = context.new_page()
        
        try:
            page.goto(job_url, wait_until="networkidle")
            random_delay()
            
            if platform == "handshake":
                print("[Auto-Apply] Detected Handshake job post.")
                _apply_handshake(page, user_profile_data, resume_pdf_path)
            elif "lever.co" in job_url:
                print("[Auto-Apply] Detected Lever form")
                _apply_lever(page, user_profile_data, resume_pdf_path)
            
            return {"status": "success", "url": job_url}
            
        except Exception as e:
            print(f"[Auto-Apply Error] {e}")
            page.screenshot(path="apply_failure.png")
            return {"status": "failed", "error": str(e)}
        finally:
            # We don't save context here, we assume it's read-only for workers
            browser.close()

def _apply_handshake(page, user_profile_data, resume_pdf_path):
    """
    Advanced Handshake Apply Flow
    """
    # 1. Click the main "Apply" button. Handshake uses various React classes.
    try:
        # Standard fast selector attempt
        apply_btn = page.locator('button:has-text("Apply")').first
        apply_btn.wait_for(timeout=5000)
        apply_btn.click()
    except PlaywrightTimeoutError:
        print("[!] Standard Apply button not found. Attempting AI Fallback...")
        html = page.content()
        ai_sel = dynamic_selector.predict_selector(html, "The primary 'Apply' or 'Apply Externally' button for the job")
        page.locator(ai_sel).click()

    random_delay()
    
    # 2. Upload Resume if required in modal
    try:
        # Handshake usually has a specific resume upload box or uses existing profile resume.
        file_input = page.locator('input[type="file"]')
        if file_input.count() > 0:
            file_input.first.set_input_files(resume_pdf_path)
            print("[+] Resume uploaded to Handshake modal.")
    except Exception:
        pass
    
    random_delay()
    
    # 3. Answer Custom Questions
    # (Simplified for MVP, would involve parsing each label and using LLMService to generate a response)
    
    # 4. Submit
    print("[*] Handshake application drafted. Skipping final submit to prevent unwanted applications.")
    # page.locator('button:has-text("Submit Application")').click()

def _apply_lever(page, user_profile_data, resume_pdf_path):
    """
    Basic Lever Apply Flow
    """
    first_name = user_profile_data.get("first_name", "Test")
    last_name = user_profile_data.get("last_name", "User")
    email = user_profile_data.get("email", "test@example.com")
    
    page.fill("input[name='name']", f"{first_name} {last_name}")
    random_delay()
    page.fill("input[name='email']", email)
    random_delay()
    
    if os.path.exists(resume_pdf_path):
        page.set_input_files("input[type='file'][name='resume']", resume_pdf_path)
        print("[+] Uploaded Resume")
    
    print("[*] Filled Lever form. Skipping submit.")
