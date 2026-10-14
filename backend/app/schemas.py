from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PromptCreate(BaseModel):
    title: str
    description: Optional[str] = None
    body: str
    type: Optional[str] = "text"
    tags: Optional[List[str]] = []
    language: Optional[str] = "ru"
    model_params: Optional[dict] = {}
    license: Optional[str] = "cc-by"
    visibility: Optional[str] = "public"
    parent_id: Optional[str] = None

class PromptOut(BaseModel):
    id: str
    title: str
    slug: Optional[str]
    description: Optional[str]
    body: str
    tags: Optional[List[str]]
    author_id: Optional[str]
    parent_id: Optional[str]
    created_at: Optional[str]
