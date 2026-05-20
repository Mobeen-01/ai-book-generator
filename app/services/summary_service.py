from app.services.openai_service import generate_text
from app.utils.prompts import SUMMARY_PROMPT
from app.config import SUMMARY_MODEL


def summarize_chapter(content):

    prompt = SUMMARY_PROMPT.format(
        content=content
    )

    return generate_text(prompt, SUMMARY_MODEL)