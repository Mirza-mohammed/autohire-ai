import os
import uuid
from playwright.sync_api import sync_playwright

class PDFGeneratorService:
    def __init__(self):
        # We will save generated PDFs to a tmp dir to avoid cluttering the main repo
        self.output_dir = "/tmp/autohire_resumes"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_ats_pdf(self, tailored_resume_data: dict, candidate_name: str, candidate_email: str) -> str:
        """
        Takes the TailoredResume JSON (from LLMService) and generates a fresh, ATS-friendly PDF.
        Returns the absolute path to the generated PDF.
        """
        html_content = self._build_harvard_html_template(tailored_resume_data, candidate_name, candidate_email)
        filename = f"Resume_{candidate_name.replace(' ', '_')}_{str(uuid.uuid4())[:8]}.pdf"
        output_path = os.path.join(self.output_dir, filename)

        with sync_playwright() as p:
            # We use chromium headless to print the HTML exactly as it would appear on a page
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Load the HTML string directly into the browser
            page.set_content(html_content, wait_until="networkidle")
            
            # Print to PDF (Harvard ATS format prefers standard US Letter, no margins for pure content)
            page.pdf(
                path=output_path, 
                format="Letter",
                margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
                print_background=True
            )
            browser.close()

        return output_path

    def _build_harvard_html_template(self, data: dict, name: str, email: str) -> str:
        """
        Generates clean, minimalist HTML designed to be perfectly parsed by ATS systems like Workday/Greenhouse.
        """
        
        # Build Skills Section
        skills_html = f"<p><strong>Technical Skills:</strong> {', '.join(data.get('skills_to_highlight', []))}</p>"
        
        # Build Experience Section
        exp_html = ""
        for exp in data.get("tailored_experience", []):
            bullets_html = "".join([f"<li>{bullet}</li>" for bullet in exp.get("tailored_bullets", [])])
            exp_html += f"""
            <div class="experience-block">
                <div class="exp-header">
                    <strong>{exp.get("title", "Role")}</strong>
                    <span>{exp.get("company", "Company")}</span>
                </div>
                <ul>{bullets_html}</ul>
            </div>
            """

        # HTML Boilerplate with CSS embedded
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: "Times New Roman", Times, serif;
                    font-size: 11pt;
                    line-height: 1.3;
                    color: #000;
                    margin: 0;
                    padding: 0;
                }}
                h1 {{
                    font-size: 24pt;
                    text-align: center;
                    margin-bottom: 5px;
                    font-weight: normal;
                }}
                .contact-info {{
                    text-align: center;
                    font-size: 10pt;
                    margin-bottom: 20px;
                    border-bottom: 1px solid #000;
                    padding-bottom: 10px;
                }}
                h2 {{
                    font-size: 13pt;
                    border-bottom: 1px solid #000;
                    text-transform: uppercase;
                    margin-top: 15px;
                    margin-bottom: 10px;
                }}
                .experience-block {{
                    margin-bottom: 15px;
                }}
                .exp-header {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px;
                }}
                ul {{
                    margin-top: 0;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 4px;
                }}
            </style>
        </head>
        <body>
            <h1>{name}</h1>
            <div class="contact-info">
                {email} | https://linkedin.com/in/candidate
            </div>

            <h2>Skills & Technologies</h2>
            {skills_html}

            <h2>Professional Experience</h2>
            {exp_html}

        </body>
        </html>
        """
        return html
