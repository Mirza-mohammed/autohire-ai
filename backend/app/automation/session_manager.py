import os
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.join(os.path.dirname(__file__), "sessions")

class SessionManager:
    """
    Manages Playwright browser contexts to persist authentication states (cookies, local storage).
    This allows workers to bypass 2FA and SSO walls.
    """
    
    def __init__(self):
        os.makedirs(SESSION_DIR, exist_ok=True)
    
    def get_session_path(self, platform_name: str) -> str:
        return os.path.join(SESSION_DIR, f"{platform_name}_storage_state.json")

    def interactive_login(self, platform_name: str, login_url: str):
        """
        Opens a visible browser for the user to manually log in.
        Once they close the browser, the session is saved.
        """
        state_path = self.get_session_path(platform_name)
        
        print(f"[*] Opening browser for {platform_name}. Please log in manually.")
        print(f"[*] Close the browser window when you are fully logged in.")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False) # MUST be False for manual login
            context = browser.new_context()
            page = context.new_page()
            
            page.goto(login_url)
            
            # Wait for the user to manually close the browser
            try:
                page.wait_for_event("close", timeout=0) # wait indefinitely
            except Exception:
                pass
                
            # Save the state before the context closes
            context.storage_state(path=state_path)
            print(f"[+] Session saved to {state_path}")
            browser.close()

    def load_context(self, browser, platform_name: str):
        """
        Loads a saved session into a new browser context.
        """
        state_path = self.get_session_path(platform_name)
        if os.path.exists(state_path):
            print(f"[*] Loading authenticated session for {platform_name}")
            return browser.new_context(storage_state=state_path)
        else:
            print(f"[!] No saved session found for {platform_name}. Starting fresh.")
            return browser.new_context()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "login":
        platform = sys.argv[2] if len(sys.argv) > 2 else "handshake"
        url = "https://joinhandshake.co.uk/login" if platform == "handshake" else "https://linkedin.com/login"
        SessionManager().interactive_login(platform, url)
