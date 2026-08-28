import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def get_required(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable is missing: {name}"
        )

    return value


@dataclass(frozen=True)
class Settings:
    # Telegram
    bot_token: str
    owner_id: int

    # Database
    database_url: str

    # Web App
    webapp_url: str

    # Security
    secret_key: str

    # Optional Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

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
