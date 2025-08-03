from fastapi import FastAPI, Request, status
from models import Base
from database import engine
from router import blog
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(blog.router)