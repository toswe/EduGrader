from openai import OpenAI as OpenAIRaw

from grading.integrations.integration import LLMIntegration


class OpenAI(LLMIntegration):
    def __init__(self):
        self.client = OpenAIRaw()  # Api key read from OPENAI_API_KEY env variable by default

    def prompt(self, input, model="gpt-4o", instructions=None, temperature=0):
        response = self.client.responses.create(
            model=model,
            instructions=instructions,
            input=input,
            temperature=temperature,
        )
        for item in response.output:
            if hasattr(item, 'content') and item.content:
                return item.content[0].text, response.to_dict()
        return None, response.to_dict()
