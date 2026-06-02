import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
ADMIN_CHAT_IDS: list[int] = [
    int(x.strip()) for x in os.getenv("ADMIN_CHAT_IDS", "").split(",") if x.strip()
]
CHANNEL_ID: str = os.getenv("CHANNEL_ID", "")
DB_PATH: str = os.getenv("DB_PATH", "data/subscribers.db")
PORT: int = int(os.getenv("PORT", "10000"))
