try:
    from grading.integrations.openai import OpenAI
    from grading.integrations.gemini import Gemini
    from grading.integrations.deepseek import DeepSeek
except ModuleNotFoundError:
    # Fallback to relative imports when running outside Django app context
    from .openai import OpenAI
    from .gemini import Gemini
    from .deepseek import DeepSeek
from enum import Enum


class Integration(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"


def get_integration(name: str):
    try:
        integration = Integration(name)
    except ValueError:
        raise ValueError(f"Unknown integration: {name}")

    if integration == Integration.OPENAI:
        return OpenAI()
    elif integration == Integration.GEMINI:
        return Gemini()
    elif integration == Integration.DEEPSEEK:
        return DeepSeek()
