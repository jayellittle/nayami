from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import posts_ref
from pydantic import BaseModel
from enum import Enum
from typing import List


app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("../frontend/index.html")

class CategoryEnum(str, Enum):
    ETC = "etc",
    STUDY = "study",
    WORK = "work",
    RELATIONSHIP = "relationship",
    LOVE = "love"

class Post(BaseModel):
    title: str
    body: str
    categories: List[CategoryEnum]

@app.post("/posts")
async def create_post(post: Post):
    new_post = {
        "title": post.title,
        "body": post.body,
        "categories": [cat.value for cat in post.categories],
        "timestamp": {'.sv': 'timestamp'}
    }
    posts_ref.push(new_post)
    return {"status": "success"}


@app.get("/posts")
async def get_posts():
    return posts_ref.order_by_child("timestamp").get()
