from app.core.celery_app import celery_app
import imaplib
import email
from email.header import decode_header
import os

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = os.getenv("GMAIL_ADDRESS", "your_email@gmail.com")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "your_app_password")

@celery_app.task
def poll_recruiter_emails():
    """
    Background task to poll Gmail for recruiter responses (Interviews, Rejections).
    """
    if EMAIL_ACCOUNT == "your_email@gmail.com":
        print("[Email Monitor] Missing Gmail credentials, skipping...")
        return
        
    print(f"[Email Monitor] Polling inbox for {EMAIL_ACCOUNT}...")
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select("inbox")
        
        # Search for recent emails containing keywords
        # UNSEEN is good, but for demo we just search for standard recruiter phrases
        status, messages = mail.search(None, '(OR (SUBJECT "Interview") (SUBJECT "Application Status"))')
        
        if status == "OK":
            email_ids = messages[0].split()
            print(f"[Email Monitor] Found {len(email_ids)} relevant emails.")
            
            for eid in email_ids[-5:]: # Check only the 5 most recent
                res, msg_data = mail.fetch(eid, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            if encoding:
                                subject = subject.decode(encoding)
                            else:
                                subject = subject.decode('utf-8')
                        
                        sender = msg.get("From")
                        print(f"[Email Monitor] From: {sender} | Subject: {subject}")
                        
                        # TODO: Trigger Agent to classify email as Interview vs Rejection
                        # and update the DB Application status accordingly.
                        
        mail.logout()
        return {"status": "success"}
    except Exception as e:
        print(f"[Email Monitor Error] {e}")
        return {"error": str(e)}
