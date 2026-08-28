"""
Secret Village
Database Models

SQLAlchemy models for:

- Users
- Media
- Media versions
- Secrets
- Favorites
- Gifts
- Settings
- Sessions
- OAuth accounts
- Activity / audit logs

Security:
- No bot tokens stored here
- No passwords or raw secrets in audit logs
- Sensitive operations should be handled transactionally
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    BigInteger,
    String,
    Text,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database import Base


# ============================================================
# COMMON HELPERS
# ============================================================

def utcnow() -> datetime:
    return datetime.utcnow()


# ============================================================
# USER
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    username: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    display_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        default="bn",
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="USER",
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_premium: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    storage_limit: Mapped[int] = mapped_column(
        BigInteger,
        default=100 * 1024 * 1024,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    last_active_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Relationships
    files: Mapped[list["File"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    secrets: Mapped[list["Secret"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    gifts: Mapped[list["Gift"]] = relationship(
        back_populates="recipient",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_users_username_display_name",
            "username",
            "display_name",
        ),
    )


# ============================================================
# FILE / MEDIA
# ============================================================

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    telegram_file_id: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    telegram_file_unique_id: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        index=True,
    )

    file_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    filename: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    mime_type: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    size: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    width: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    height: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    duration: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    caption: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    thumbnail_file_id: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates="files",
    )

    versions: Mapped[list["FileVersion"]] = relationship(
        back_populates="file",
        cascade="all, delete-orphan",
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="file",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_files_owner_type_created",
            "owner_id",
            "file_type",
            "created_at",
        ),
        Index(
            "ix_files_owner_deleted",
            "owner_id",
            "is_deleted",
        ),
    )


# ============================================================
# FILE VERSION
# ============================================================

class FileVersion(Base):
    __tablename__ = "file_versions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    telegram_file_id: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    size: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    file: Mapped["File"] = relationship(
        back_populates="versions",
    )


# ============================================================
# SECRET
# ============================================================

class Secret(Base):
    __tablename__ = "secrets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    secret_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    max_views: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates="secrets",
    )

    views: Mapped[list["SecretView"]] = relationship(
        back_populates="secret",
        cascade="all, delete-orphan",
    )


# ============================================================
# SECRET VIEW
# ============================================================

class SecretView(Base):
    __tablename__ = "secret_views"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    secret_id: Mapped[int] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    viewer_telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )

    viewed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    secret: Mapped["Secret"] = relationship(
        back_populates="views",
    )


# ============================================================
# FAVORITE
# ============================================================

class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="favorites",
    )

    file: Mapped["File"] = relationship(
        back_populates="favorites",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "file_id",
            name="uq_user_file_favorite",
        ),
    )


# ============================================================
# OAUTH ACCOUNT
# ============================================================

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    provider_user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_oauth_provider_user",
        ),
    )


# ============================================================
# ACTIVITY / AUDIT LOG
# ============================================================

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    actor_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    target_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    target_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    result: Mapped[str] = mapped_column(
        String(30),
        default="success",
        nullable=False,
    )

    details: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
        index=True,
    )


# ============================================================
# GIFT
# ============================================================

class Gift(Base):
    __tablename__ = "gifts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    gift_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    value: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    max_uses: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    used_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    recipient: Mapped["User"] = relationship(
        back_populates="gifts",
    )


# ============================================================
# SETTINGS
# ============================================================

class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    key: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    value: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    value_type: Mapped[str] = mapped_column(
        String(30),
        default="string",
        nullable=False,
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )


# ============================================================
# SESSION
# ============================================================

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    session_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    device_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="sessions",
    )


# ============================================================
# MODEL EXPORTS
# ============================================================

__all__ = [
    "User",
    "File",
    "FileVersion",
    "Secret",
    "SecretView",
    "Favorite",
    "OAuthAccount",
    "ActivityLog",
    "Gift",
    "Setting",
    "Session",
  ]
