import json
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup
import re

class SelectorPrediction(BaseModel):
    selector: str = Field(description="The exact Playwright-compatible CSS or Text selector to locate the requested element.")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0.")

class DynamicSelectorEngine:
    def __init__(self):
        self.is_mock = False
        try:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            self.structured_llm = self.llm.with_structured_output(SelectorPrediction)
        except Exception:
            self.is_mock = True
        
    def clean_html(self, raw_html: str) -> str:
        """Strip scripts, styles, and SVGs to save tokens before sending to LLM."""
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup(["script", "style", "svg", "noscript", "meta"]):
            tag.decompose()
            
        # Remove empty tags
        for tag in soup.find_all(lambda t: not t.contents and not t.name == 'input'):
            tag.extract()
            
        # Minify somewhat
        html = str(soup)
        html = re.sub(r'\s+', ' ', html).strip()
        return html

    def predict_selector(self, raw_html: str, element_description: str) -> str:
        """
        Uses an LLM to predict the CSS/Text selector for an element described by natural language.
        """
        if self.is_mock:
            print(f"[*] [MOCK] Asking AI for selector for: '{element_description}'")
            return "button"

        cleaned_html = self.clean_html(raw_html)
        
        # If the HTML is still too huge, we should ideally chunk it or only take the body.
        # For this deep dive, we'll assume it fits in context (gpt-4o-mini has 128k context).
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert web automation engineer. You are given a chunk of HTML and a description of an element a bot needs to click or type into. Your task is to return the most reliable Playwright-compatible selector (e.g. `button:has-text('Apply')`, `input[name='email']`, or a unique class). Focus on accessibility roles, aria-labels, and specific text."),
            ("human", "HTML:\n{html}\n\nElement Description to find: {description}")
        ])
        
        chain = prompt | self.structured_llm
        
        print(f"[*] Asking AI for selector for: '{element_description}'")
        prediction = chain.invoke({"html": cleaned_html, "description": element_description})
        
        print(f"[+] AI suggested selector: '{prediction.selector}' (Confidence: {prediction.confidence})")
        return prediction.selector

dynamic_selector = DynamicSelectorEngine()
