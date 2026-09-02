import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATABASE_PATH = Path(
    os.getenv("RESOLVEAI_DB_PATH", str(BASE_DIR / "resolveai.db"))
)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("RESOLVEAI_CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
