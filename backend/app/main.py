from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, auth
from .database import SessionLocal, engine, Base
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Remix Hub MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created = crud.create_user(db, user)
    access_token = auth.create_access_token({"sub": created.id})
    return {"access_token": access_token, "token_type":"bearer"}

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = auth.create_access_token({"sub": user.id})
    return {"access_token": access_token, "token_type":"bearer"}

@app.post("/auth/apple")
def apple_placeholder():
    return {"detail": "Apple Sign-In must be configured in production. See README."}

@app.post("/prompts", response_model=schemas.PromptOut)
def create_prompt(prompt: schemas.PromptCreate, db: Session = Depends(get_db), authorization: str | None = Header(default=None)):
    # Simplified auth: extract bearer token to get author id; fallback to 'anonymous'
    author_id = "anonymous"
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split()[1]
        try:
            from jose import jwt
            payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
            author_id = payload.get("sub", "anonymous")
        except Exception:
            author_id = "anonymous"
    db_prompt = crud.create_prompt(db, prompt, author_id)
    return db_prompt

@app.get("/prompts")
def list_prompts(q: str = None, limit:int=20, offset:int=0, db: Session = Depends(get_db)):
    items = crud.list_prompts(db, q, limit, offset)
    return items

@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str, db: Session = Depends(get_db)):
    p = crud.get_prompt(db, prompt_id)
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    return p

@app.post("/prompts/{prompt_id}/remix", response_model=schemas.PromptOut)
def remix(prompt_id: str, payload: schemas.PromptCreate, db: Session = Depends(get_db)):
    author_id = "anonymous"
    newp = crud.remix_prompt(db, prompt_id, payload.dict(), author_id)
    if not newp:
        raise HTTPException(status_code=404, detail="Original prompt not found")
    return newp
