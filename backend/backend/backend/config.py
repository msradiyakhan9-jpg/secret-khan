import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # Telegram Bot Token & Owner
    bot_token: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    owner_id: int = int(os.getenv("OWNER_ID", "123456789")) # আপনার টেলিগ্রাম ID
    
    # Database URL
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./vault.db")

settings = Settings()
