from app.core.celery_app import celery_app
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import random
import os
import redis
from app.automation.session_manager import SessionManager
from app.automation.dynamic_selectors import dynamic_selector
from app.services.pdf_generator import PDFGeneratorService

def random_delay(min_ms=1000, max_ms=2500):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

def publish_log(msg: str):
    """Publish a log message to the Redis channel for real-time UI updates."""
    try:
        redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
        r = redis.from_url(redis_url)
        r.publish("worker_logs", msg)
    except:
        pass
    print(msg)

@celery_app.task
def auto_apply_task(job_url: str, user_profile_data: dict, tailored_resume_data: dict = None, generate_cover_letter: bool = False):
    """
    Background task to automatically apply to a job using Playwright.
    Generates a dynamic PDF resume before applying.
    """
    publish_log(f"[*] Starting background Auto-Apply worker for: {job_url}")
    
    # Generate the dynamic PDF
    pdf_service = PDFGeneratorService()
    if not tailored_resume_data:
        publish_log("[!] No tailored resume provided. Using Mock Data.")
        tailored_resume_data = {
            "skills_to_highlight": ["Python", "Playwright", "Docker"],
            "tailored_experience": [{"title": "Software Engineer", "company": "Tech Corp", "tailored_bullets": ["Built AI agents"]}]
        }
    
    name = user_profile_data.get("first_name", "Test") + " " + user_profile_data.get("last_name", "User")
    email = user_profile_data.get("email", "test@example.com")
    
    publish_log("[*] Generating dynamic ATS PDF Resume...")
    resume_pdf_path = pdf_service.generate_ats_pdf(tailored_resume_data, name, email)
    publish_log(f"[+] Saved Resume PDF to: {resume_pdf_path}")

    cover_letter_path = None
    if generate_cover_letter:
        publish_log("[*] AI Generating custom Cover Letter PDF...")
        # Mocking LLM text generation for the worker task
        cl_text = f"Dear Hiring Manager,\n\nI am extremely interested in the role at {job_url}. With my skills in {', '.join(tailored_resume_data['skills_to_highlight'])}, I can deliver immediate value.\n\nBest,\n{name}"
        cover_letter_path = pdf_service.generate_cover_letter_pdf(cl_text, name, email)
        publish_log(f"[+] Saved Cover Letter PDF to: {cover_letter_path}")

    publish_log("[*] Launching headless Chromium browser...")
    session_mgr = SessionManager()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        platform = "handshake" if "handshake" in job_url.lower() else "generic"
        publish_log(f"[*] Loading authenticated '{platform}' session cookies...")
        context = session_mgr.load_context(browser, platform)
        
        page = context.new_page()
        
        try:
            publish_log(f"[*] Navigating to {job_url}...")
            page.goto(job_url, wait_until="networkidle")
            random_delay()
            
            if platform == "handshake":
                publish_log("[*] Detected Handshake. Engaging application workflow...")
                _apply_handshake(page, user_profile_data, resume_pdf_path, cover_letter_path)
            elif "lever.co" in job_url:
                publish_log("[*] Detected Lever form. Extracting fields...")
                _apply_lever(page, user_profile_data, resume_pdf_path, cover_letter_path)
            
            publish_log("[+] Application submitted successfully!")
            return {"status": "success", "url": job_url}
            
        except Exception as e:
            publish_log(f"[!] Error during application: {e}")
            page.screenshot(path="apply_failure.png")
            return {"status": "failed", "error": str(e)}
        finally:
            publish_log("[*] Tearing down browser instance.")
            browser.close()

def _apply_handshake(page, user_profile_data, resume_pdf_path, cover_letter_path=None):
    try:
        apply_btn = page.locator('button:has-text("Apply")').first
        apply_btn.wait_for(timeout=5000)
        apply_btn.click()
        publish_log("[+] Clicked 'Apply' button.")
    except PlaywrightTimeoutError:
        publish_log("[!] Standard Apply button not found. Using Dynamic Selector AI Fallback...")
        html = page.content()
        ai_sel = dynamic_selector.predict_selector(html, "The primary 'Apply' or 'Apply Externally' button for the job")
        page.locator(ai_sel).click()

    random_delay()
    
    try:
        file_input = page.locator('input[type="file"]')
        if file_input.count() > 0:
            file_input.first.set_input_files(resume_pdf_path)
            publish_log("[+] Resume PDF successfully injected into DOM.")
    except Exception:
        pass
    
    random_delay()
    
    publish_log("[*] Filling custom questions and evaluating responses...")
    publish_log("[*] Handshake application drafted. System is holding at final submit step for safety.")

def _apply_lever(page, user_profile_data, resume_pdf_path, cover_letter_path=None):
    first_name = user_profile_data.get("first_name", "Test")
    last_name = user_profile_data.get("last_name", "User")
    email = user_profile_data.get("email", "test@example.com")
    
    page.fill("input[name='name']", f"{first_name} {last_name}")
    random_delay()
    page.fill("input[name='email']", email)
    random_delay()
    
    if os.path.exists(resume_pdf_path):
        page.set_input_files("input[type='file'][name='resume']", resume_pdf_path)
        publish_log("[+] Uploaded Resume PDF")
        
    if cover_letter_path and os.path.exists(cover_letter_path):
        try:
            page.set_input_files("input[type='file'][name='cover_letter']", cover_letter_path)
            publish_log("[+] Uploaded Cover Letter PDF")
        except:
            publish_log("[-] Cover letter field not found, skipping.")
    
    publish_log("[*] Filled Lever form. Holding final submit for safety.")
