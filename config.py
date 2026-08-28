"""
Application Configuration
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # ========================================================
    # Telegram
    # ========================================================

    bot_token: str = os.getenv("BOT_TOKEN",8406688505:AAGkmKI4rUagmq7n9wlV30ZodOAWecZZRAo "")
    owner_id: int = int(os.getenv("OWNER_ID", "8547982063"))

    # ========================================================
    # Database
    # ========================================================

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"
    )

    # ========================================================
    # Application
    # ========================================================

    environment: str = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    app_name: str = os.getenv(
        "APP_NAME",
        "Secret Village"
    )

    debug: bool = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"

    # ========================================================
    # Media
    # ========================================================

    default_page_size: int = int(
        os.getenv("DEFAULT_PAGE_SIZE", "10")
    )

    max_page_size: int = int(
        os.getenv("MAX_PAGE_SIZE", "50")
    )

    max_upload_size_mb: int = int(
        os.getenv("MAX_UPLOAD_SIZE_MB", "100")
    )

    # ========================================================
    # Security
    # ========================================================

    session_expiry_hours: int = int(
        os.getenv("SESSION_EXPIRY_HOURS", "168")
    )

    max_login_attempts: int = int(
        os.getenv("MAX_LOGIN_ATTEMPTS", "5")
    )

    # ========================================================
    # Feature Defaults
    # ========================================================

    maintenance_mode: bool = os.getenv(
        "MAINTENANCE_MODE",
        "false"
    ).lower() == "true"

    photos_enabled: bool = True
    videos_enabled: bool = True
    audio_enabled: bool = True
    documents_enabled: bool = True
    search_enabled: bool = True
    favorites_enabled: bool = True
    secrets_enabled: bool = True


settings = Settings()    google_redirect_uri: str

    # Application
    app_name: str
    environment: str
    debug: bool

    # Upload limits
    max_file_size_mb: int

    # Secret defaults
    default_secret_expiry_hours: int


def load_settings() -> Settings:
    return Settings(
        bot_token=get_required("BOT_TOKEN"),

        owner_id=int(get_required("OWNER_ID")),

        database_url=os.getenv(
            "DATABASE_URL",
            "sqlite+aiosqlite:///./secret_vault.db"
        ),

        webapp_url=os.getenv(
            "WEBAPP_URL",
            ""
        ),

        secret_key=get_required("SECRET_KEY"),

        google_client_id=os.getenv(
            "GOOGLE_CLIENT_ID",
            ""
        ),

        google_client_secret=os.getenv(
            "GOOGLE_CLIENT_SECRET",
            ""
        ),

        google_redirect_uri=os.getenv(
            "GOOGLE_REDIRECT_URI",
            ""
        ),

        app_name=os.getenv(
            "APP_NAME",
            "Secret Vault"
        ),

        environment=os.getenv(
            "ENVIRONMENT",
            "development"
        ),

        debug=os.getenv(
            "DEBUG",
            "false"
        ).lower() == "true",

        max_file_size_mb=int(
            os.getenv(
                "MAX_FILE_SIZE_MB",
                "2000"
            )
        ),

        default_secret_expiry_hours=int(
            os.getenv(
                "DEFAULT_SECRET_EXPIRY_HOURS",
                "24"
            )
        ),
    )


settings = load_settings()
