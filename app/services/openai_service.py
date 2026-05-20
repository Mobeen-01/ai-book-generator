from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

def generate_text(prompt, model="llama-3.3-70b-versatile"):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
