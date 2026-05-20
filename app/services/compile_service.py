from app.utils.exporters import (
    export_docx,
    export_pdf,
    export_txt
)


def compile_book(book_title, chapters):

    docx_path = export_docx(book_title, chapters)
    pdf_path = export_pdf(book_title, chapters)
    txt_path = export_txt(book_title, chapters)

    return {
        "docx": docx_path,
        "pdf": pdf_path,
        "txt": txt_path
    }