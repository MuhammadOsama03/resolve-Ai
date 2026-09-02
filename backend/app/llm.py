import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import GEMINI_API_KEY, GEMINI_MODEL


def generate_gemini_reply(prompt: str, timeout: float = 20.0) -> str | None:
    """Generate a reply with Gemini when an API key is configured.

    Returning None keeps the application usable without external credentials
    and lets the copilot fall back to its deterministic grounded composer.
    """
    if not GEMINI_API_KEY:
        return None

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    body = json.dumps(
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 500},
        }
    ).encode("utf-8")
    request = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None

    try:
        parts = payload["candidates"][0]["content"]["parts"]
        text = "\n".join(part.get("text", "") for part in parts).strip()
        return text or None
    except (KeyError, IndexError, TypeError):
        return None
