
import json
import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Book Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');

/* ── Reset & root ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0f0e0c !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Main container ── */
[data-testid="stMain"] > div {
    padding: 0 !important;
}
.block-container {
    max-width: 860px !important;
    margin: 0 auto !important;
    padding: 3rem 2rem 6rem !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    margin-bottom: 4rem;
    padding-bottom: 2.5rem;
    border-bottom: 0.5px solid rgba(232,228,220,0.12);
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #b8a97a;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 600;
    color: #f5f0e6;
    line-height: 1.1;
    margin: 0 0 0.6rem;
    letter-spacing: -0.01em;
}
.hero-sub {
    font-size: 15px;
    color: #8c8880;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* ── Step cards ── */
.step-card {
    background: #1a1916;
    border: 0.5px solid rgba(232,228,220,0.1);
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #b8a97a;
    margin-bottom: 0.4rem;
    display: block;
}
.step-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 400;
    color: #f0ece2;
    margin: 0 0 1.5rem;
}

/* ── Section dividers ── */
.divider {
    height: 0.5px;
    background: rgba(232,228,220,0.08);
    margin: 2.5rem 0;
    border: none;
}

/* ── Input overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #0f0e0c !important;
    border: 0.5px solid rgba(232,228,220,0.18) !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #b8a97a !important;
    box-shadow: 0 0 0 2px rgba(184,169,122,0.12) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    color: #8c8880 !important;
    text-transform: uppercase !important;
    font-family: 'DM Mono', monospace !important;
    margin-bottom: 6px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: #b8a97a !important;
    color: #0f0e0c !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 0.6rem 1.5rem !important;
    letter-spacing: 0.04em !important;
    transition: background 0.2s, transform 0.1s !important;
    cursor: pointer !important;
}
[data-testid="stButton"] > button:hover {
    background: #cfc08e !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: scale(0.98) translateY(0) !important;
}

/* ── Alert boxes ── */
[data-testid="stSuccess"] {
    background: rgba(26,78,48,0.35) !important;
    border: 0.5px solid rgba(78,160,98,0.35) !important;
    border-radius: 10px !important;
    color: #a3ddb4 !important;
    font-size: 13px !important;
}
[data-testid="stError"] {
    background: rgba(80,20,20,0.4) !important;
    border: 0.5px solid rgba(200,80,80,0.3) !important;
    border-radius: 10px !important;
    color: #f0a0a0 !important;
    font-size: 13px !important;
}

/* ── Info badge ── */
.book-id-badge {
    display: inline-block;
    background: rgba(184,169,122,0.12);
    border: 0.5px solid rgba(184,169,122,0.3);
    color: #b8a97a;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    border-radius: 6px;
    padding: 4px 12px;
    margin-top: 0.5rem;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    color: #b8a97a !important;
}

/* ── Chapter display ── */
.chapter-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #f0ece2;
    margin: 0 0 0.3rem;
    font-weight: 400;
}
.chapter-meta {
    font-size: 12px;
    color: #6b6660;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}

/* ── JSON/outline display ── */
[data-testid="stTextArea"] textarea[readonly] {
    background: #121110 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    line-height: 1.7 !important;
    color: #a8a098 !important;
}

/* ── Subheader overrides ── */
h2, h3 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 400 !important;
    color: #f0ece2 !important;
    letter-spacing: -0.01em !important;
}

/* ── Completion banner ── */
.completion-banner {
    background: linear-gradient(135deg, rgba(26,78,48,0.4), rgba(16,50,30,0.4));
    border: 0.5px solid rgba(78,160,98,0.4);
    border-radius: 14px;
    padding: 1.5rem 2rem;
    text-align: center;
}
.completion-banner .icon { font-size: 2rem; margin-bottom: 0.5rem; }
.completion-banner p {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #a3ddb4;
    margin: 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(184,169,122,0.25); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(184,169,122,0.45); }

/* ── Write section ── */
[data-testid="stWrite"] { color: #8c8880 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by AI</div>
    <h1 class="hero-title">Book Generator</h1>
    <p class="hero-sub">Craft full-length books — outline, chapters, and compilation — in one workflow.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 1 — CREATE BOOK
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-card">
    <span class="step-label">Step 01</span>
    <p class="step-title">Create your book</p>
</div>
""", unsafe_allow_html=True)

title = st.text_input("Book title", placeholder="e.g. The Art of Thinking Clearly")
# notes = st.text_area(
#     "Outline notes",
#     height=120,
#     placeholder="Describe the tone, themes, intended audience, or any structural ideas…"
# )

# if st.button("Create Book →"):
#     with st.spinner("Creating book…"):
#         res = requests.post(
#             f"{API}/create-book",
#             json={"title": title}
#             # json={"title": title, "notes_on_outline_before": notes}
#             # "notes_on_outline_before": "" 
            
            
#         )
#     if res.status_code != 200:
#         st.error(res.text)
#         st.stop()
#     data = res.json()
#     book = data["data"][0]
#     st.session_state["book_id"] = book["id"]
#     st.success("Book created successfully.")
#     st.markdown(f'<div class="book-id-badge">ID: {book["id"]}</div>', unsafe_allow_html=True)


if st.button("Create Book →"):
    with st.spinner("Creating book…"):
        res = requests.post(
            f"{API}/create-book",
            json={"title": title}
        )

    # ❌ handle HTTP failure first
    if res.status_code != 200:
        st.error(res.text)
        st.stop()

    data = res.json()

    # ❌ safe checks (THIS fixes your crash)
    if "data" not in data or not data["data"]:
        st.error(data.get("error", "Invalid API response: missing data"))
        st.write(data)  # debug help
        st.stop()

    book = data["data"][0]

    st.session_state["book_id"] = book["id"]
    st.success("Book created successfully.")
    st.markdown(
        f'<div class="book-id-badge">ID: {book["id"]}</div>',
        unsafe_allow_html=True
    )
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 2 — GENERATE OUTLINE
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-card">
    <span class="step-label">Step 02</span>
    <p class="step-title">Generate outline</p>
</div>
""", unsafe_allow_html=True)

st.text_area(
    "Outline Notes (Required before generating outline)",
    key="outline_notes_before"
)

notes_before = st.session_state.get("outline_notes_before", "")

if st.button("Generate Outline"):
    book_id = st.session_state.get("book_id")

    if not book_id:
        st.error("Create a book first")
        st.stop()

    if not notes_before.strip():
        st.error("Outline notes are required before generating outline")
        st.stop()

    with st.spinner("Generating outline..."):
        res = requests.post(
            f"{API}/generate-outline/{book_id}",
            json={
                "notes": notes_before   # optional backend use
            }
        )
        data = res.json()
        st.session_state["outline"] = data["outline"]
        st.success("Outline generated.")
        
# if st.button("Generate Outline →"):
#     book_id = st.session_state.get("book_id")
#     if not book_id:
#         st.error("Create a book first.")
#         st.stop()
#     with st.spinner("Generating outline…"):
#         res = requests.post(f"{API}/generate-outline/{book_id}")
#     if res.status_code != 200:
#         st.error(res.text)
#         st.stop()
    # data = res.json()
    # st.session_state["outline"] = data["outline"]
    # st.success("Outline generated.")

if "outline" in st.session_state:
    st.text_area(
        "Outline (JSON)",
        json.dumps(st.session_state["outline"], indent=2),
        height=400
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 3 — IMPROVE OUTLINE
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-card">
    <span class="step-label">Step 03 — Optional</span>
    <p class="step-title">Improve outline</p>
</div>
""", unsafe_allow_html=True)

notes_after = st.text_area(
    "Improvement notes",
    height=120,
    placeholder="Suggestions for restructuring, adding chapters, changing tone…"
)

if st.button("Update Outline →"):
    book_id = st.session_state.get("book_id")
    if not book_id:
        st.error("Create a book first.")
        st.stop()
    with st.spinner("Updating outline…"):
        res = requests.post(
            f"{API}/update-outline/{book_id}",
            json={"notes_on_outline_after": notes_after}
        )
    if res.status_code != 200:
        st.error(res.text)
        st.stop()
    data = res.json()
    updated_outline = data["outline"]
    if isinstance(updated_outline, str):
        try:
            updated_outline = json.loads(updated_outline)
        except:
            pass
    st.session_state["outline"] = updated_outline
    st.success("Outline updated.")
    st.text_area(
        "Updated outline",
        json.dumps(updated_outline, indent=2),
        height=400
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 4 — GENERATE NEXT CHAPTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-card">
    <span class="step-label">Step 04</span>
    <p class="step-title">Generate next chapter</p>
</div>
""", unsafe_allow_html=True)

if st.button("Generate Next Chapter →"):
    book_id = st.session_state.get("book_id")
    if not book_id:
        st.error("Create a book first.")
        st.stop()
    with st.spinner("Generating chapter…"):
        res = requests.post(f"{API}/generate-next-chapter/{book_id}")
    if res.status_code != 200:
        st.error(res.text)
        st.stop()
    data = res.json()
    st.session_state["current_chapter"] = data
    st.success("Chapter generated.")

if "current_chapter" in st.session_state:
    ch = st.session_state["current_chapter"]
    if ch.get("status") == "completed":
        st.markdown("""
        <div class="completion-banner">
            <div class="icon">✦</div>
            <p>All chapters have been generated</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p class="chapter-header">Chapter {ch['chapter_number']}: {ch['chapter_title']}</p>
        <p class="chapter-meta">Generated content below</p>
        """, unsafe_allow_html=True)
        st.text_area("Content", ch["content"], height=460)
        st.text_area("Summary", ch["summary"], height=180)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="step-card">
            <span class="step-label">Chapter feedback</span>
            <p class="step-title">Improve this chapter</p>
        </div>
        """, unsafe_allow_html=True)

        feedback = st.text_area(
            "Improvement notes for this chapter",
            height=120,
            placeholder="What would you like changed or improved in this chapter?"
        )

        if st.button("Save Chapter Feedback →"):
            with st.spinner("Saving feedback…"):
                res = requests.post(
                    f"{API}/chapter-feedback/{ch['chapter_id']}",
                    json={"chapter_notes": feedback}
                )
            if res.status_code != 200:
                st.error(res.text)
                st.stop()
            st.success("Feedback saved. Generate the chapter again to apply.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 5 — LOAD ALL CHAPTERS
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-card">
    <span class="step-label">Step 05</span>
    <p class="step-title">Review all chapters</p>
</div>
""", unsafe_allow_html=True)

if st.button("Load All Chapters →"):
    book_id = st.session_state.get("book_id")
    res = requests.get(f"{API}/chapters/{book_id}")
    if res.status_code != 200:
        st.error(res.text)
        st.stop()
    st.session_state["chapters"] = res.json()

if "chapters" in st.session_state:
    for ch in st.session_state["chapters"]:
        st.markdown(f"""
        <p class="chapter-header" style="margin-top:1.5rem;">
            Chapter {ch['chapter_number']}: {ch['chapter_title']}
        </p>
        <p class="chapter-meta">ID: {ch['id']}</p>
        """, unsafe_allow_html=True)
        st.text_area(
            f"Content — Ch. {ch['chapter_number']}",
            ch["content"] or "",
            height=280,
            key=f"content_{ch['id']}"
        )
        st.text_area(
            f"Summary — Ch. {ch['chapter_number']}",
            ch["summary"] or "",
            height=100,
            key=f"summary_{ch['id']}"
        )

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 6 — COMPILE BOOK
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-card">
    <span class="step-label">Step 06</span>
    <p class="step-title">Compile finished book</p>
</div>
""", unsafe_allow_html=True)

# if st.button("Compile Book →"):
#     book_id = st.session_state.get("book_id")
#     with st.spinner("Compiling…"):
#         res = requests.post(f"{API}/compile-book/{book_id}")
#     if res.status_code != 200:
#         st.error(res.text)
#         st.stop()
#     data = res.json()
#     st.success("Book compiled successfully.")
#     st.text_area("Full compiled book", data["compiled_book"], height=600)

if st.button("Compile Book →"):
    book_id = st.session_state.get("book_id")

    with st.spinner("Compiling PDF…"):
        res = requests.post(f"{API}/compile-book/{book_id}")

    if res.status_code != 200:
        st.error(res.text)
        st.stop()

    # data = res.json()

    # st.success("Book compiled successfully.")

    # with open(data["pdf"], "rb") as f:
    #     st.download_button(
    #         "📥 Download PDF",
    #         f,
    #         file_name="book.pdf"
    #     )
    
    data = res.json()

    st.success("Book compiled successfully.")

    with open(data["pdf"], "rb") as f:
        pdf_bytes = f.read()

    st.markdown("""
    <style>
    [data-testid="stDownloadButton"] > button {
        width: 100% !important;
        background: transparent !important;
        border: 0.5px solid rgba(184,169,122,0.4) !important;
        color: #b8a97a !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.06em !important;
        padding: 0.75rem 1.5rem !important;
        margin-top: 0.5rem !important;
        transition: background 0.2s, border-color 0.2s !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: rgba(184,169,122,0.08) !important;
        border-color: rgba(184,169,122,0.7) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.download_button(
        "↓  Download PDF",
        pdf_bytes,
        file_name="book.pdf",
        mime="application/pdf",
    )
        
        
        
        
    # data = res.json()

    # st.success("Book compiled successfully.")

    # pdf_path = data["pdf_path"]

    # with open(pdf_path, "rb") as f:
    #     st.download_button(
    #         label="📥 Download PDF",
    #         data=f,
    #         file_name="book.pdf",
    #         mime="application/pdf"
    #     )















# import json
# import streamlit as st
# import requests

# API = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="AI Book Generator",
#     layout="wide"
# )

# st.title("📚 AI Book Generator System")

# # =========================================================
# # CREATE BOOK
# # =========================================================
# st.header("1. Create Book")

# title = st.text_input("Book Title")

# notes = st.text_area(
#     "Outline Notes",
#     height=150
# )

# if st.button("Create Book"):

#     with st.spinner("Creating book..."):

#         res = requests.post(
#             f"{API}/create-book",
#             json={
#                 "title": title,
#                 "notes_on_outline_before": notes
#             }
#         )

#     if res.status_code != 200:

#         st.error(res.text)
#         st.stop()

#     data = res.json()

#     book = data["data"][0]

#     st.session_state["book_id"] = book["id"]

#     st.success("✅ Book Created")

#     st.write("Book ID:", book["id"])


# # =========================================================
# # GENERATE OUTLINE
# # =========================================================
# st.header("2. Generate Outline")

# if st.button("Generate Outline"):

#     book_id = st.session_state.get("book_id")

#     if not book_id:

#         st.error("Create a book first")
#         st.stop()

#     with st.spinner("Generating outline..."):

#         res = requests.post(
#             f"{API}/generate-outline/{book_id}"
#         )

#     if res.status_code != 200:

#         st.error(res.text)
#         st.stop()

#     data = res.json()

#     st.session_state["outline"] = data["outline"]

#     st.success("✅ Outline Generated")


# # =========================================================
# # SHOW OUTLINE
# # =========================================================
# if "outline" in st.session_state:

#     st.subheader("📄 Generated Outline")

#     st.text_area(
#         "Outline JSON",
#         json.dumps(
#             st.session_state["outline"],
#             indent=2
#         ),
#         height=450
#     )


# # =========================================================
# # UPDATE OUTLINE
# # =========================================================
# st.header("3. Improve Outline (Optional)")

# notes_after = st.text_area(
#     "Improvement Notes",
#     height=150
# )

# if st.button("Update Outline"):

#     book_id = st.session_state.get("book_id")

#     if not book_id:

#         st.error("Create a book first")
#         st.stop()

#     with st.spinner("Updating outline..."):

#         res = requests.post(
#             f"{API}/update-outline/{book_id}",
#             json={
#                 "notes_on_outline_after": notes_after
#             }
#         )

#     if res.status_code != 200:

#         st.error(res.text)
#         st.stop()

#     data = res.json()

#     updated_outline = data["outline"]

#     # if returned as string
#     if isinstance(updated_outline, str):

#         try:
#             updated_outline = json.loads(updated_outline)
#         except:
#             pass

#     st.session_state["outline"] = updated_outline

#     st.success("✅ Outline Updated")

#     st.text_area(
#         "Updated Outline",
#         json.dumps(
#             updated_outline,
#             indent=2
#         ),
#         height=450
#     )


# # =========================================================
# # GENERATE NEXT CHAPTER
# # =========================================================
# st.header("4. Generate Next Chapter")

# if st.button("Generate Next Chapter"):

#     book_id = st.session_state.get("book_id")

#     if not book_id:

#         st.error("Create a book first")
#         st.stop()

#     with st.spinner("Generating chapter..."):

#         res = requests.post(
#             f"{API}/generate-next-chapter/{book_id}"
#         )

#     if res.status_code != 200:

#         st.error(res.text)
#         st.stop()

#     data = res.json()

#     st.session_state["current_chapter"] = data

#     st.success("✅ Chapter Generated")


# # =========================================================
# # SHOW CURRENT CHAPTER
# # =========================================================
# if "current_chapter" in st.session_state:

#     ch = st.session_state["current_chapter"]

#     if ch.get("status") == "completed":

#         st.success("🎉 All chapters generated")

#     else:

#         st.subheader(
#             f"📘 Chapter {ch['chapter_number']}: {ch['chapter_title']}"
#         )

#         st.text_area(
#             "Chapter Content",
#             ch["content"],
#             height=500
#         )

#         st.text_area(
#             "Chapter Summary",
#             ch["summary"],
#             height=200
#         )

#         # =========================================================
#         # CHAPTER FEEDBACK
#         # =========================================================
#         st.subheader("✍️ Chapter Feedback")

#         feedback = st.text_area(
#             "Improvement Notes For This Chapter",
#             height=150
#         )

#         if st.button("Save Chapter Feedback"):

#             with st.spinner("Saving feedback..."):

#                 res = requests.post(
#                     f"{API}/chapter-feedback/{ch['chapter_id']}",
#                     json={
#                         "chapter_notes": feedback
#                     }
#                 )

#             if res.status_code != 200:

#                 st.error(res.text)
#                 st.stop()

#             st.success(
#                 "✅ Feedback saved. Generate chapter again."
#             )


# # =========================================================
# # LOAD ALL CHAPTERS
# # =========================================================
# st.header("5. Load All Chapters")

# if st.button("Load Chapters"):

#     # res = requests.get(
#     #     f"{API}/chapters"
#     # )

#     book_id = st.session_state.get("book_id")

#     res = requests.get(
#         f"{API}/chapters/{book_id}"
#     )
#     if res.status_code != 200:

#         st.error(res.text)
#         st.stop()

#     st.session_state["chapters"] = res.json()


# if "chapters" in st.session_state:

#     st.subheader("📚 All Chapters")

#     for ch in st.session_state["chapters"]:

#         st.markdown(
#             f"## Chapter {ch['chapter_number']}: {ch['chapter_title']}"
#         )

#         st.text_area(
#             f"content_{ch['id']}",
#             ch["content"] or "",
#             height=300
#         )

#         st.text_area(
#             f"summary_{ch['id']}",
#             ch["summary"] or "",
#             height=120
#         )


# # =========================================================
# # COMPILE BOOK
# # =========================================================
# st.header("6. Compile Book")

# if st.button("Compile Book"):
#     book_id = st.session_state.get("book_id")
#     with st.spinner("Compiling book..."):

#         res = requests.post(
            

#             f"{API}/compile-book/{book_id}"
#         )

#     if res.status_code != 200:

#         st.error(res.text)
#         st.stop()

#     st.success("✅ Book Compiled")

#     st.write("Check outputs folder")
    
    
#     data = res.json()

#     st.text_area(
#         "Compiled Book",
#         data["compiled_book"],
#         height=600
#     )

    