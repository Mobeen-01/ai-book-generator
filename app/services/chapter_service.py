from app.services.openai_service import generate_text
from app.utils.prompts import CHAPTER_PROMPT


def generate_chapter(
    title,
    outline,
    summaries,
    chapter_title,
    sections,
    chapter_number,
    notes=""
):

    prompt = CHAPTER_PROMPT.format(

        title=title,

        outline=outline,

        summaries=summaries,

        chapter_title=chapter_title,

        sections=sections,

        chapter_number=chapter_number,

        notes=notes

    )

    return generate_text(prompt)