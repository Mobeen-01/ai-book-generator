from app.db import supabase

from app.services.compile_service import compile_book

from app.services.notification_service import (
    send_teams_message,
    send_email
)


def run_final_workflow():

    books = supabase.table("books") \
        .select("*") \
        .execute()

    for book in books.data:

        # Skip if final review not approved
        if book["final_review_notes_status"] not in [
            "no_notes_needed",
            "yes"
        ]:
            continue

        # Get all chapters
        chapters_response = supabase.table("chapters") \
            .select("*") \
            .eq("book_id", book["id"]) \
            .order("chapter_number") \
            .execute()

        chapters = chapters_response.data

        # Skip if no chapters found
        if not chapters:
            print(f"No chapters found for {book['title']}")
            continue

        # Compile book outputs
        outputs = compile_book(
            book["title"],
            chapters
        )

        # Update book status
        supabase.table("books") \
            .update({
                "book_output_status": "completed"
            }) \
            .eq("id", book["id"]) \
            .execute()

        # Teams notification
        send_teams_message(
            f"""
            Book Compiled Successfully

            Title: {book['title']}

            Files Generated:
            DOCX: {outputs['docx']}
            PDF: {outputs['pdf']}
            TXT: {outputs['txt']}
            """
        )

        # Optional Email Notification
        send_email(
            subject="Book Compilation Completed",
            body=f"""
Book Title: {book['title']}

Generated Files:

DOCX:
{outputs['docx']}

PDF:
{outputs['pdf']}

TXT:
{outputs['txt']}
            """,
            to_email="editor@example.com"
        )

        print(f"Book compiled: {book['title']}")