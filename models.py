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
