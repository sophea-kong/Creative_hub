from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(String(255))
    type = Column(String(255))
    media_url = Column(String(255), nullable=True)
    tags = Column(String(255))
    # created_at = Column(datetime)

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(255), nullable=False)
    # uploaded_at = Column(TIMESTAMP)