from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.db import supabase
from app.services.outline_service import generate_outline
from app.workflows.chapter_workflow import generate_next_chapter
from app.services.pdf_service import generate_pdf
import json
import uuid
import os
from app.services.notification_dispatcher import NotificationDispatcher

app = FastAPI(title="Automated Book Generator")
notifier = NotificationDispatcher()

# ----------------------------
# MODELS
# ----------------------------
class CreateBookRequest(BaseModel):
    title: str
    # notes_on_outline_before: str = ""


class UpdateOutlineRequest(BaseModel):
    notes_on_outline_after: str

class OutlineRequest(BaseModel):
    notes: str = ""

# ----------------------------
# HEALTH
# ----------------------------
@app.get("/")
def home():
    return {"message": "Book Generator Running"}


# ----------------------------
# CREATE BOOK
# ----------------------------
@app.post("/create-book")
def create_book(data: CreateBookRequest):

    try:
        response = supabase.table("books").insert({
            "title": data.title,
            # "notes_on_outline_before": data.notes_on_outline_before,
            "status_outline_notes": "no_notes_needed",
            "final_review_notes_status": "no_notes_needed",
            "book_output_status": "pending"
        }).execute()

        return {"message": "Book created", "data": response.data}

    except Exception as e:
        return {"error": str(e)}




import json

# ----------------------------
# GENERATE OUTLINE
# ----------------------------
@app.post("/generate-outline/{book_id}")
# def generate_outline_route(book_id: str):
def generate_outline_route(book_id: str, data: OutlineRequest):

    # VALIDATION
    if not book_id or book_id == "None":

        raise HTTPException(
            status_code=400,
            detail="Invalid book_id"
        )

    # GET BOOK
    book_res = supabase.table("books") \
        .select("*") \
        .eq("id", book_id) \
        .single() \
        .execute()

    if not book_res.data:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book = book_res.data

    # GENERATE OUTLINE
    # outline = generate_outline(
    #     book["title"],
    #     book.get("notes_on_outline_before", "")
    # )
    outline = generate_outline(
        book["title"],
        data.notes
    )

    # SAVE OUTLINE
    supabase.table("books") \
        .update({
            "outline": outline,
            "status_outline_notes": "generated",
            "notes_on_outline_before": data.notes
        }) \
        .eq("id", book_id) \
        .execute()

    # ---------------------------------
    # PARSE OUTLINE JSON
    # ---------------------------------
    try:

        outline_json = json.loads(outline)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON returned by AI: {str(e)}"
        )

    # ---------------------------------
    # DELETE OLD CHAPTERS
    # useful when regenerating outline
    # ---------------------------------
    supabase.table("chapters") \
        .delete() \
        .eq("book_id", book_id) \
        .execute()

    # ---------------------------------
    # CREATE CHAPTER ROWS
    # ---------------------------------
    for chapter in outline_json["chapters"]:

        supabase.table("chapters") \
            .insert({

                "book_id": book_id,

                "chapter_number": chapter["chapter_id"],

                "chapter_title": chapter["chapter_title"],

                "content": "",

                "summary": "",

                "chapter_notes": "",

                "chapter_notes_status": "no_notes",

                "generation_status": "pending"

            }) \
            .execute()
    notifier.trigger(
        "OUTLINE_READY",
        receiver_email="muhammadmobeentahir@gmail.com",
        extra_message=f"Book: {book['title']} outline generated"
    )
    # RESPONSE
    return {

        "message": "Outline generated successfully",

        "book_id": book_id,

        "outline": outline_json,

        "total_chapters": len(
            outline_json["chapters"]
        ),

        "ui_state": "OUTLINE_READY"
    }
    
    
# ----------------------------
# UPDATE OUTLINE (HUMAN FEEDBACK LOOP)
# ----------------------------
@app.post("/update-outline/{book_id}")
def update_outline(book_id: str, data: UpdateOutlineRequest):

    if not book_id or book_id == "None":

        raise HTTPException(
            status_code=400,
            detail="Invalid book_id"
        )

    # GET BOOK
    book_res = supabase.table("books") \
        .select("*") \
        .eq("id", book_id) \
        .single() \
        .execute()

    if not book_res.data:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book = book_res.data

    # GENERATE UPDATED OUTLINE
    updated_outline = generate_outline(

        book["title"],

        data.notes_on_outline_after

    )

    # SAVE OUTLINE
    supabase.table("books") \
        .update({

            "outline": updated_outline,

            "notes_on_outline_after":
                data.notes_on_outline_after,

            "status_outline_notes": "updated"

        }) \
        .eq("id", book_id) \
        .execute()

    # PARSE JSON
    try:

        outline_json = json.loads(updated_outline)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON: {str(e)}"
        )

    # DELETE OLD CHAPTERS
    supabase.table("chapters") \
        .delete() \
        .eq("book_id", book_id) \
        .execute()

    # CREATE NEW CHAPTERS
    for chapter in outline_json["chapters"]:

        supabase.table("chapters") \
            .insert({

                "book_id": book_id,

                "chapter_number": chapter["chapter_id"],

                "chapter_title": chapter["chapter_title"],

                "content": "",

                "summary": "",

                "chapter_notes": "",

                "chapter_notes_status": "no_notes",

                "generation_status": "pending"

            }) \
            .execute()
    notifier.trigger(
        "OUTLINE_READY",
        receiver_email="muhammadmobeentahir@gmail.com",
        extra_message="Outline updated after user feedback"
    )
    return {

        "book_id": book_id,

        "outline": outline_json,

        "ui_state": "OUTLINE_UPDATED"
    }

# ----------------------------
# GET OUTLINE (UI)
# ----------------------------
@app.get("/outline/{book_id}")
def get_outline(book_id: str):

    res = supabase.table("books") \
        .select("id, title, outline") \
        .eq("id", book_id) \
        .single() \
        .execute()

    if not res.data:
        raise HTTPException(status_code=404, detail="Book not found")

    return res.data


# ----------------------------
# GET CHAPTERS BY BOOK
# ----------------------------
@app.get("/chapters/{book_id}")
def get_chapters(book_id: str):

    res = supabase.table("chapters") \
        .select("*") \
        .eq("book_id", book_id) \
        .order("chapter_number") \
        .execute()

    return res.data

# ----------------------------
# GENERATE NEXT CHAPTER
# ----------------------------
@app.post("/generate-next-chapter/{book_id}")
def generate_next_chapter_route(book_id: str):

    if not book_id or book_id == "None":

        raise HTTPException(
            status_code=400,
            detail="Invalid book_id"
        )

    result = generate_next_chapter(book_id)
    notifier.trigger(
        "CHAPTER_WAITING",
        receiver_email="muhammadmobeentahir@gmail.com",
        extra_message="System waiting for chapter notes/input"
    )
    return result

# ----------------------------
# SAVE CHAPTER FEEDBACK
# ----------------------------
class ChapterFeedbackRequest(BaseModel):
    chapter_notes: str
    
    
@app.post("/chapter-feedback/{chapter_id}")
def chapter_feedback(
    chapter_id: str,
    data: ChapterFeedbackRequest
):

    supabase.table("chapters") \
        .update({

            "chapter_notes": data.chapter_notes,

            "content": "",

            "summary": "",
            
            "chapter_notes_status": "yes",
            

            "generation_status": "pending"

        }) \
        .eq("id", chapter_id) \
        .execute()

    return {
        "message": "Feedback saved"
    }
    

@app.post("/compile-book/{book_id}")
def compile_book(book_id: str):

    book_res = supabase.table("books") \
        .select("*") \
        .eq("id", book_id) \
        .single() \
        .execute()

    chapters_res = supabase.table("chapters") \
        .select("*") \
        .eq("book_id", book_id) \
        .order("chapter_number") \
        .execute()

    book = book_res.data
    chapters = chapters_res.data

    structured_chapters = []

    for ch in chapters:

        raw_content = ch.get("content")

        if isinstance(raw_content, str) and raw_content.strip():
            try:
                # Strip markdown code fences if AI wrapped the JSON in them
                cleaned = raw_content.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("```")[1]  # remove opening ```json or ```
                    if cleaned.startswith("json"):
                        cleaned = cleaned[4:]          # strip the word "json"
                cleaned = cleaned.strip()
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                parsed = {}
        else:
            parsed = {}
        # -----------------------
        # SAFE SECTION EXTRACTION
        # -----------------------
        sections = []
        try:
            sections = parsed.get("chapters", [{}])[0].get("sections", [])
        except Exception:
            sections = []

        structured_chapters.append({
            "chapter_id": ch["chapter_number"],
            "chapter_title": ch["chapter_title"],
            "sections": sections
        })

    # -----------------------
    # GENERATE PDF
    # -----------------------
    file_name = f"{book_id}.pdf"
    file_path = os.path.join("outputs", file_name)

    os.makedirs("outputs", exist_ok=True)
   
    pdf_path = generate_pdf(
        title=book["title"],
        chapters=structured_chapters,
        output_path=file_path
    )
    notifier.trigger(
        "FINAL_DRAFT_READY",
        receiver_email="muhammadmobeentahir@gmail.com",
        extra_message=f"PDF ready: {pdf_path}"
    )
    return {
        "book_title": book["title"],
        "pdf": pdf_path,
        "message": "PDF generated successfully"
    }