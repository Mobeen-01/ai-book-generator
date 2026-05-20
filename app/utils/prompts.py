OUTLINE_PROMPT = """
You are a professional book outlining assistant.

Book Title:
{title}

Editor Notes:
{notes}

Your task is to create a detailed, structured book outline.

Requirements:
1. Break the book into chapters.
2. Assign a unique numeric ID to each chapter (e.g., 1, 2, 3...).
3. Each chapter should contain a simple list of section titles.
4. Return ONLY valid JSON.

JSON Structure Format:
{{
  "book_title": "...",
  "chapters": [
    {{
      "chapter_id": 1,
      "chapter_title": "...",
      "sections": [
        "Section title 1",
        "Section title 2"
      ]
    }}
  ]
}}

Rules:
- Output must be ONLY JSON.
- No extra text.
"""


CHAPTER_PROMPT = """
You are a professional book writing assistant.

Book Title:
{title}

Full Book Outline:
{outline}

Current Chapter Number:
{chapter_number}

Current Chapter Title:
{chapter_title}

Current Chapter Sections:
{sections}

Previous Chapter Summaries:
{summaries}

Editor Notes:
{notes}

TASK:
Write a complete detailed chapter.

RULES:
- Follow the chapter sections strictly.
- Maintain continuity using previous chapter summaries.
- Write naturally like a real book.
- Do not repeat previous chapters.

Return ONLY this JSON format:

{{
  "chapters": [
    {{
      "chapter_id": 1,
      "chapter_title": "Introduction to Keys",
      "sections": [
        {{
          "title": "What are Keys",
          "content": "..."
        }},
        {{
          "title": "History of Keys",
          "content": "..."
        }},
        {{
          "title": "Types of Keys",
          "content": "..."
        }}
      ]
    }}
  ]
}}
"""
SUMMARY_PROMPT = """
You are an expert book summarizer.

Your task is to summarize the following chapter content.

Rules:
- Keep summary concise
- Capture key ideas only
- Do not add extra commentary

Chapter Content:
{content}

Return only the summary text.
"""

