import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# =========================================================
# LOAD LOCAL .ENV
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# =========================================================
# GET GROQ API KEY
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# If environment variable is not available,
# try Streamlit Secrets.
if not GROQ_API_KEY:

    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

    except Exception:
        GROQ_API_KEY = None


# =========================================================
# CHECK API KEY
# =========================================================

if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY not found. "
        "Add it to your local .env file or "
        "Streamlit Cloud Secrets."
    )


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# GENERATE READING VERSION
# =========================================================

def generate_reading_version(
    transcript: str,
    language: str = "English"
) -> str:

    prompt = f"""
You are an expert English editor and educational
content writer.

Transform the following YouTube transcript into a
natural English reading version.

The purpose of this text is English learning.

The user will listen to the original video while
reading this version. Preserve the important meaning,
information, explanations, examples, events, and ideas.

The final result should read like a book chapter,
magazine article, or well-written educational article.

It must NOT feel like a YouTube script.

LANGUAGE:

{language}

WRITING STYLE:

Use natural English, clear sentences, smooth
transitions, well-connected ideas, natural vocabulary,
and complete paragraphs.

OUTPUT FORMAT:

Write ONLY normal paragraphs.

Do NOT use:

- Headings
- Subheadings
- Titles
- Bullet points
- Numbered lists
- Markdown
- Hashtags
- Bold text
- Italic text
- Asterisks
- ### symbols
- Horizontal lines
- Timestamps
- Time ranges
- Speaker labels
- Narrator labels
- Camera directions
- Visual directions
- Scene directions
- Stage directions
- [Music]
- [Applause]
- [Visual]
- [Camera]
- Hook:
- Introduction:
- Conclusion:
- Narrator:
- Speaker 1:
- Speaker 2:

Do not put every sentence on a separate line.

Write several complete paragraphs.

Separate paragraphs with one blank line.

Do not copy the transcript sentence by sentence.

Rewrite the content naturally in your own words.

Preserve the original meaning.

Do not invent facts.

Do not add unsupported information.

Remove unnecessary YouTube-specific phrases such as
"Welcome back to the channel", "Like and subscribe",
and "Stay tuned" when they do not contribute to the
actual subject matter.

The final text should be useful for:

Reading practice
Listening practice
Shadowing practice
Vocabulary development
Speaking practice

Return ONLY the rewritten reading text.

SOURCE TRANSCRIPT:

{transcript}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert English editor. "
                    "Return only natural paragraph-based "
                    "reading material."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    reading_version = response.choices[0].message.content

    if not reading_version:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    return reading_version.strip()