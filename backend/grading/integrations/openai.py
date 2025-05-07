from openai import OpenAI as OpenAIRaw


class OpenAI:
    def __init__(self):
        self.client = OpenAIRaw()  # Api key read from OPENAI_API_KEY env variable by default

    def prompt(self, input, model="gpt-4o", instructions=None):
        return self.client.responses.create(
            model=model,
            instructions=instructions,
            input=input,
        )
