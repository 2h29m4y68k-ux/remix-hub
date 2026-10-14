from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
import uuid
from .database import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, index=True)
    slug = Column(String, index=True)
    description = Column(Text)
    body = Column(Text)
    input_schema = Column(JSON, nullable=True)
    example_input = Column(JSON, nullable=True)
    example_output = Column(Text, nullable=True)
    type = Column(String, default="text")
    tags = Column(JSON, nullable=True)
    language = Column(String, default="ru")
    model_params = Column(JSON, nullable=True)
    visibility = Column(String, default="public")
    license = Column(String, default="cc-by")
    author_id = Column(String, ForeignKey("users.id"))
    parent_id = Column(String, nullable=True)
    lineage = Column(JSON, nullable=True)
    fork_count = Column(Integer, default=0)
    remix_count = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
