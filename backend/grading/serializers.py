from rest_framework import serializers
from grading.models import AnswerGrade


def _response_text(llm_response):
    """The model's raw answer, dug out of whichever provider shape llm_response was stored in."""
    if isinstance(llm_response, str):
        return llm_response

    if not isinstance(llm_response, dict):
        return ""

    # OpenAI responses API.
    for item in llm_response.get("output", []):
        for content in item.get("content", []):
            if content.get("text"):
                return content["text"]

    # DeepSeek (and any other chat completions API).
    for choice in llm_response.get("choices", []):
        content = choice.get("message", {}).get("content")
        if content:
            return content

    return ""


class AnswerGradeSerializer(serializers.ModelSerializer):
    explanation = serializers.SerializerMethodField()

    def get_explanation(self, obj):
        # The prompt asks for the score on the first line and the reasoning below it.
        text = _response_text(obj.llm_response)
        head, _, rest = text.partition("\n")
        return (rest if head.strip().isdigit() else text).strip()

    class Meta:
        model = AnswerGrade
        fields = "__all__"
