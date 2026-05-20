from app.db import supabase
from app.services.outline_service import generate_outline
from app.services.notification_service import (
    send_email,
    send_teams_message
)


def run_outline_workflow():

    books = supabase.table("books") \
        .select("*") \
        .execute()

    for book in books.data:

        if not book["notes_on_outline_before"]:
            continue

        outline = generate_outline(
            book["title"],
            book["notes_on_outline_before"]
        )

        supabase.table("books") \
            .update({
                "outline": outline
            }) \
            .eq("id", book["id"]) \
            .execute()

        send_teams_message(
            f"Outline ready for {book['title']}"
        )