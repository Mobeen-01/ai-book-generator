import json

from app.db import supabase

from app.services.chapter_service import generate_chapter
from app.services.summary_service import summarize_chapter


# -----------------------------------
# GET PREVIOUS SUMMARIES
# -----------------------------------
def get_previous_summaries(
    book_id,
    current_chapter_number
):

    response = supabase.table("chapters") \
        .select("summary") \
        .eq("book_id", book_id) \
        .lt("chapter_number", current_chapter_number) \
        .execute()

    summaries = []

    for row in response.data:

        if row["summary"]:
            summaries.append(row["summary"])

    return "\n\n".join(summaries)


# -----------------------------------
# GENERATE NEXT CHAPTER
# -----------------------------------
def generate_next_chapter(book_id):

    # -----------------------------------
    # GET BOOK
    # -----------------------------------
    book_response = supabase.table("books") \
        .select("*") \
        .eq("id", book_id) \
        .single() \
        .execute()

    if not book_response.data:

        return {
            "error": "Book not found"
        }

    book = book_response.data

    # -----------------------------------
    # GET NEXT PENDING CHAPTER
    # -----------------------------------
    chapter_response = supabase.table("chapters") \
        .select("*") \
        .eq("book_id", book_id) \
        .eq("generation_status", "pending") \
        .order("chapter_number") \
        .limit(1) \
        .execute()

    # ALL DONE
    if not chapter_response.data:

        return {
            "status": "completed",
            "message": "All chapters generated"
        }

    chapter = chapter_response.data[0]

    # -----------------------------------
    # LOAD OUTLINE JSON
    # -----------------------------------
    # outline_json = json.loads(
    #     book["outline"]
    # )
    
    outline_data = book["outline"]

    if isinstance(outline_data, str):

        outline_json = json.loads(outline_data)

    else:

        outline_json = outline_data

    # -----------------------------------
    # FIND CURRENT CHAPTER SECTIONS
    # -----------------------------------
    current_sections = []

    for ch in outline_json["chapters"]:

        if ch["chapter_id"] == chapter["chapter_number"]:

            current_sections = ch["sections"]
            break

    # -----------------------------------
    # GET PREVIOUS SUMMARIES
    # -----------------------------------
    previous_summaries = get_previous_summaries(
        book_id,
        chapter["chapter_number"]
    )

    # -----------------------------------
    # GENERATE CHAPTER CONTENT
    # -----------------------------------
    content = generate_chapter(

        title=book["title"],

        outline=book["outline"],

        summaries=previous_summaries,

        chapter_title=chapter["chapter_title"],

        sections="\n".join(current_sections),

        chapter_number=chapter["chapter_number"],

        notes=chapter.get("chapter_notes", "")

    )

    # -----------------------------------
    # GENERATE SUMMARY
    # -----------------------------------
    summary = summarize_chapter(content)

    # -----------------------------------
    # SAVE IN DATABASE
    # -----------------------------------
    supabase.table("chapters") \
        .update({

            "content": content,

            "summary": summary,

            "generation_status": "generated"

        }) \
        .eq("id", chapter["id"]) \
        .execute()

    # -----------------------------------
    # RETURN RESPONSE
    # -----------------------------------
    return {

        "status": "generated",

        "chapter_id": chapter["id"],

        "chapter_number": chapter["chapter_number"],

        "chapter_title": chapter["chapter_title"],

        "content": content,

        "summary": summary
    }