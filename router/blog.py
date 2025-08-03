from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
from models import Post
from database import SessionLocal
# from .auth import get_current_user
# from starlette.responses import RedirectResponse
# from fastapi.templating import Jinja2Templates

# templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class post_create(BaseModel):
    title :str
    content : str
    type : str
    tag : str

@router.get("/",status_code=status.HTTP_200_OK)
async def readAll(db:db_dependency):
    allblog = db.query(Post).all()
    return allblog

@router.post("/create-post",status_code=status.HTTP_201_CREATED)
async def create_post(db:db_dependency, post_req:post_create):
    post_model = Post(
        title = post_req.title,
        content = post_req.content,
        type =  post_req.type,
        tags = post_req.tag
                      )
    db.add(post_model)
    db.commit()

@router.put("/edit-post", status_code=status.HTTP_200_OK)
async def edit_post(db : db_dependency,post_id : int, post_req:post_create):
    post_model = db.query(Post).filter(post_id == Post.id).first()
    post_model.title = post_req.title
    post_model.content = post_req.content
    post_model.type = post_req.content
    post_model.tags = post_req.tag
    db.add(post_model)
    db.commit()