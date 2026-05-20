# AI Book Generator

An automated book generation system that uses AI (Groq/LLaMA) to write full books chapter by chapter — with a human feedback loop at each step. Books are stored in Supabase and exported as PDFs. Email notifications are sent at key stages.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| AI Model | Groq (LLaMA 3.3 70B) |
| Database | Supabase (Postgres) |
| PDF Export | ReportLab |
| Notifications | SMTP Email |

## Key Features

- **Outline Generation** — AI generates a structured chapter outline from a book title
- **Human Feedback Loop** — Review and provide notes before each chapter is written
- **Chapter-by-Chapter Writing** — AI writes one chapter at a time using context from previous summaries
- **PDF Compilation** — All chapters compiled into a downloadable PDF
- **Email Notifications** — Automated emails at outline ready, chapter waiting, and final draft stages

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_email_app_password
```

### 4. Set up Supabase tables

Create two tables in your Supabase project:

**`books`** — `id, title, outline, status_outline_notes, notes_on_outline_before, notes_on_outline_after, final_review_notes_status, book_output_status`

**`chapters`** — `id, book_id, chapter_number, chapter_title, content, summary, chapter_notes, chapter_notes_status, generation_status`

### 5. Run the backend

```bash
uvicorn app.main:app --reload
```

### 6. Run the frontend (new terminal)

```bash
streamlit run ui/streamlit_app.py
```

The API runs on `http://localhost:8000` and the UI on `http://localhost:8501`.
