from datetime import datetime
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), nullable=True)
    role = Column(String(20), default="USER") # OWNER, ADMIN, USER
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    files = relationship("File", back_populates="owner", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_number = Column(Integer, index=True)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
    file_id = Column(String(255), nullable=False)
    category = Column(String(32), nullable=False) # photo, video, voice, document
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="files")

class Setting(Base):
    __tablename__ = "settings"

    key = Column(String(64), primary_key=True)
    value = Column(Text, nullable=False)
