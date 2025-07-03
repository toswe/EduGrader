from google import genai
from google.genai import types

from grading.integrations.integration import LLMIntegration


class Gemini(LLMIntegration):
    def __init__(self):
        self.client = genai.Client()  # Api key read from GOOGLE_API_KEY env variable by default

    def prompt(self, input, model="gemini-2.5-flash", instructions=None):
        response = self.client.models.generate_content(
            model=model,
            contents=input,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
            ),
        )
        return response.text
