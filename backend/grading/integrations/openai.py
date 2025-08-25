from openai import OpenAI as OpenAIRaw

from grading.integrations.integration import LLMIntegration


class OpenAI(LLMIntegration):
    def __init__(self):
        self.client = OpenAIRaw()  # Api key read from OPENAI_API_KEY env variable by default

    def prompt(self, input, model="gpt-4o", instructions=None):
        response = self.client.responses.create(
            model=model,
            instructions=instructions,
            input=input,
        )
        return response.output[0].content[0].text, response.to_dict()
