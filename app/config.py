import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SUMMARY_MODEL = "llama-3.3-70b-versatile"