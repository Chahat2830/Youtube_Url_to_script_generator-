import streamlit as st

from services.transcript import get_transcript
from services.groq_ai import generate_reading_version
from utils.text_cleaner import clean_transcript


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="YouTube English Reader",
    page_icon="📖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .info-box {
        padding: 18px;
        border-radius: 10px;
        background-color: rgba(128, 128, 128, 0.08);
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📖 YouTube English Reader</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Turn YouTube videos into natural English reading material'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 Reading Settings")

    language = st.selectbox(
        "Output Language",
        [
            "English"
        ]
    )

    reading_style = st.selectbox(
        "Reading Style",
        [
            "Natural English",
            "Simple English",
            "Detailed English"
        ]
    )

    st.divider()

    st.markdown(
        """
        **How to use**

        1. Paste a YouTube video URL.
        2. Extract the transcript.
        3. Convert it into natural English.
        4. Read while listening to the video.
        5. Use the text for shadowing practice.
        """
    )


# =========================================================
# YOUTUBE URL INPUT
# =========================================================

st.markdown(
    '<div class="section-title">🔗 YouTube Video</div>',
    unsafe_allow_html=True
)

youtube_url = st.text_input(
    "Paste YouTube URL",
    placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX"
)


# =========================================================
# GENERATE BUTTON
# =========================================================

generate_button = st.button(
    "📖 Generate Reading Version",
    type="primary",
    use_container_width=True
)


# =========================================================
# MAIN PIPELINE
# =========================================================

if generate_button:

    # -----------------------------------------------------
    # VALIDATE URL
    # -----------------------------------------------------

    if not youtube_url.strip():

        st.warning(
            "Please paste a YouTube video URL first."
        )

        st.stop()


    # -----------------------------------------------------
    # PROCESS VIDEO
    # -----------------------------------------------------

    with st.status(
        "Processing video...",
        expanded=True
    ) as status:

        try:

            # =============================================
            # STEP 1 — EXTRACT TRANSCRIPT
            # =============================================

            st.write(
                "🔎 Extracting transcript..."
            )

            transcript = get_transcript(
                youtube_url
            )

            if not transcript:

                status.update(
                    label="Transcript not found",
                    state="error"
                )

                st.error(
                    "No transcript could be extracted "
                    "from this video."
                )

                st.stop()


            # =============================================
            # STEP 2 — CLEAN TRANSCRIPT
            # =============================================

            st.write(
                "🧹 Cleaning transcript..."
            )

            cleaned_transcript = clean_transcript(
                transcript
            )

            if not cleaned_transcript:

                status.update(
                    label="Transcript is empty",
                    state="error"
                )

                st.error(
                    "The extracted transcript is empty."
                )

                st.stop()


            # =============================================
            # STEP 3 — GENERATE READING VERSION
            # =============================================

            st.write(
                "🤖 Converting transcript into "
                "natural English..."
            )

            reading_text = generate_reading_version(
                transcript=cleaned_transcript,
                language=language
            )


            if not reading_text:

                status.update(
                    label="Generation failed",
                    state="error"
                )

                st.error(
                    "The AI returned an empty response."
                )

                st.stop()


            # =============================================
            # PROCESS COMPLETE
            # =============================================

            status.update(
                label="Reading version generated successfully!",
                state="complete"
            )


        except Exception as e:

            status.update(
                label="Something went wrong",
                state="error"
            )

            st.error(
                f"Error: {str(e)}"
            )

            st.stop()


    # =====================================================
    # DISPLAY READING VERSION
    # =====================================================

    st.markdown(
        '<div class="section-title">📖 Reading Version</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Read this text while listening to the original "
        "video for reading and shadowing practice."
    )

    st.text_area(
        "English Reading Text",
        value=reading_text,
        height=650,
        label_visibility="collapsed"
    )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.download_button(
        label="⬇️ Download Reading Text",
        data=reading_text,
        file_name="english_reading.txt",
        mime="text/plain",
        use_container_width=True
    )