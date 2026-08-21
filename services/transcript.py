from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID&t=120
    """

    if not url or not url.strip():
        raise ValueError("YouTube URL cannot be empty.")

    url = url.strip()

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    # -----------------------------------------------------
    # Standard YouTube URL
    # -----------------------------------------------------

    if hostname in ["www.youtube.com", "youtube.com"]:

        video_id = parse_qs(parsed_url.query).get("v")

        if video_id:
            return video_id[0]

    # -----------------------------------------------------
    # Short YouTube URL
    # -----------------------------------------------------

    if hostname == "youtu.be":

        video_id = parsed_url.path.strip("/")

        if video_id:
            return video_id.split("/")[0]

    # -----------------------------------------------------
    # Invalid URL
    # -----------------------------------------------------

    raise ValueError(
        "Invalid YouTube URL. Please enter a valid YouTube video link."
    )


def get_transcript(url: str) -> str:
    """
    Extract the transcript from a YouTube video
    and return it as plain text.
    """

    # Get video ID
    video_id = extract_video_id(url)

    # Create YouTube Transcript API client
    api = YouTubeTranscriptApi()

    try:

        # Fetch transcript
        transcript = api.fetch(video_id)

    except Exception as e:

        raise RuntimeError(
            f"Could not extract transcript from this video: {str(e)}"
        )

    # -----------------------------------------------------
    # Convert transcript snippets into plain text
    # -----------------------------------------------------

    text_parts = []

    for snippet in transcript:
        text = snippet.text.strip()

        if text:
            text_parts.append(text)

    # Join everything into one continuous text
    full_text = " ".join(text_parts)

    # Final validation
    if not full_text.strip():

        raise RuntimeError(
            "The video transcript is empty."
        )

    return full_text.strip()