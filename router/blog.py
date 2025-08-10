from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.staticfiles import StaticFiles
from starlette import status
from models import Post, Image
from database import SessionLocal
# from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import shutil
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/blog',
    tags=['blog']
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

@router.get("/home",status_code= status.HTTP_200_OK)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/",status_code=status.HTTP_200_OK)
async def readAll(db:db_dependency):
    allblog = db.query(Post).all()
    return allblog

@router.get("/view_post{post_id}",status_code=status.HTTP_200_OK)
async def view_post(db:db_dependency,post_id : int):
    post_model = db.query(Post).filter(post_id == Post.id).first()
    return post_model

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
    if post_model is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Post not found.")
    post_model.title = post_req.title
    post_model.content = post_req.content
    post_model.type = post_req.content
    post_model.tags = post_req.tag
    db.add(post_model)
    db.commit()

@router.delete("/delete-post",status_code=status.HTTP_200_OK)
async def delete_post(db :db_dependency, post_id : int):
    post_model = db.query(Post).filter(post_id == Post.id).first()
    if post_model is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Post not found.")
    db.delete(post_model)
    db.commit()


UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = SessionLocal()
    image = Image(filename=file.filename, filepath=file_location)
    db.add(image)
    db.commit()
    db.refresh(image)
    db.close()

    return {"filename": file.filename, "id": image.id}

@router.get("/image/{image_id}")
def get_image(image_id: int):
    db = SessionLocal()
    image = db.query(Image).filter(Image.id == image_id).first()
    db.close()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image.filepath)
