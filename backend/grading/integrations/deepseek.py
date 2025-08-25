import os

from openai import OpenAI as OpenAIRaw

from grading.integrations.integration import LLMIntegration


class DeepSeek(LLMIntegration):
    def __init__(self):
        self.client = OpenAIRaw(
            api_key=os.getenv("DEEPSEEK_API_KEY", None),
            base_url="https://api.deepseek.com",
        )

    def prompt(self, input, model="deepseek-chat", instructions=None):
        result = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": input},
            ],
        )
        return result.choices[0].message.content, result.to_dict()
