import google.generativeai as genai
from .config import Config
from .prompts import Prompts

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL_NAME,
            system_instruction=Prompts.SYSTEM_INSTRUCTION
        )

    def analyze_diff(self, diff_text: str, title: str, description: str) -> str:
        """
        Sends the diff to Gemini and returns the review text.
        """
        prompt = Prompts.generate_review_prompt(diff_text, title, description)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"