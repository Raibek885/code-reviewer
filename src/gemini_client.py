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

    def analyze_diff(self, diff_text: str, title: str, description: str, extra_context: str = "") -> str:
        """
        Sends the diff and optional context to Gemini.
        """
        prompt = Prompts.generate_review_prompt(diff_text, title, description, extra_context)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"