from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# Database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {},
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base model
Base = declarative_base()


def get_db():
    """
    Database session dependency.
    Always close the session after use.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_database():
    """
    Create all database tables.
    """
    # Import models before creating tables
    from models import (
        User,
        File,
        FileVersion,
        Secret,
        SecretView,
        Favorite,
        OAuthAccount,
        ActivityLog,
        Gift,
        Setting,
        Session
    )

    Base.metadata.create_all(bind=engine)


def reset_database():
    """
    Development-only helper.

    WARNING:
    This deletes all database tables.
    Do NOT call this in production.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
