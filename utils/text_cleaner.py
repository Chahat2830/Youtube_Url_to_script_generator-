import re


def clean_transcript(text: str) -> str:
    """
    Clean and normalize the extracted YouTube transcript.
    """

    if not text:
        return ""

    # Remove common transcript markers
    text = re.sub(
        r"\[(?:music|applause|laughter|laughs|inaudible)\]",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove HTML tags if present
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    # Remove repeated punctuation
    text = re.sub(r"([.!?]){2,}", r"\1", text)

    # Strip unnecessary whitespace
    text = text.strip()

    return text