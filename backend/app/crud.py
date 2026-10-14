from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from slugify import slugify

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed, display_name=user.display_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_prompt(db: Session, prompt: schemas.PromptCreate, author_id: str):
    slug = slugify(prompt.title)[:100]
    db_prompt = models.Prompt(
        title=prompt.title,
        slug=slug,
        description=prompt.description,
        body=prompt.body,
        type=prompt.type,
        tags=prompt.tags,
        language=prompt.language,
        model_params=prompt.model_params,
        license=prompt.license,
        visibility=prompt.visibility,
        author_id=author_id,
        parent_id=prompt.parent_id
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompt(db: Session, prompt_id: str):
    return db.query(models.Prompt).filter(models.Prompt.id==prompt_id).first()

def list_prompts(db: Session, q: str = None, limit: int=20, offset:int=0):
    query = db.query(models.Prompt).filter(models.Prompt.visibility=="public")
    if q:
        like = f"%{q}%"
        query = query.filter((models.Prompt.title.ilike(like)) | (models.Prompt.body.ilike(like)))
    return query.order_by(models.Prompt.created_at.desc()).offset(offset).limit(limit).all()

def remix_prompt(db: Session, prompt_id: str, new_data: dict, author_id: str):
    original = get_prompt(db, prompt_id)
    if not original:
        return None
    # create new prompt with parent_id and lineage
    parent_id = original.id
    lineage = (original.lineage or []) + [original.id]
    db_prompt = models.Prompt(
        title=new_data.get("title", original.title + " (remix)"),
        slug=new_data.get("slug"),
        description=new_data.get("description", original.description),
        body=new_data.get("body", original.body),
        type=new_data.get("type", original.type),
        tags=new_data.get("tags", original.tags),
        language=new_data.get("language", original.language),
        model_params=new_data.get("model_params", original.model_params),
        license=new_data.get("license", original.license),
        visibility=new_data.get("visibility", original.visibility),
        author_id=author_id,
        parent_id=parent_id,
        lineage=lineage
    )
    db.add(db_prompt)
    original.remix_count = (original.remix_count or 0) + 1
    db.commit()
    db.refresh(db_prompt)
    return db_prompt
