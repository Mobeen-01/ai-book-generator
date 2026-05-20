import json

from app.services.openai_service import generate_text
from app.utils.prompts import OUTLINE_PROMPT


def generate_outline(title, notes):

    prompt = OUTLINE_PROMPT.format(
        title=title,
        notes=notes
    )

    response = generate_text(prompt)

    # CLEAN MARKDOWN JSON
    response = response.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    # VALIDATE JSON
    try:

        parsed = json.loads(response)

        return json.dumps(parsed)

    except Exception:

        raise Exception(
            "AI returned invalid JSON"
        )
        
        
# from app.services.openai_service import generate_text
# from app.utils.prompts import OUTLINE_PROMPT


# def generate_outline(title, notes):

#     prompt = OUTLINE_PROMPT.format(
#         title=title,
#         notes=notes
#     )

#     return generate_text(prompt)