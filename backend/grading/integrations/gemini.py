from google import genai
from google.genai import types

try:
    from grading.integrations.integration import LLMIntegration
except ModuleNotFoundError:
    # Fallback to relative import when running outside Django app context
    from .integration import LLMIntegration


class Gemini(LLMIntegration):
    def __init__(self):
        self.client = genai.Client()  # Api key read from GOOGLE_API_KEY env variable by default

    def prompt(self, input, model="gemini-2.5-flash", instructions=None):
        response = self.client.models.generate_content(
            model=model,
            contents=instructions + '\n' + input,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disables thinking
            ),
        )
        # TODO Convert full response to json
        return response.text, response.text
