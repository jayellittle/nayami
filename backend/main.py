from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import posts_ref
from pydantic import BaseModel


app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("../frontend/index.html")

class Post(BaseModel):
    content: str

@app.post("/posts")
async def create_post(post: Post):
    new_post = {
        "content": post.content,
        "timestamp": {'.sv': 'timestamp'}
    }
    posts_ref.push(new_post)
    return {"status": "success"}


@app.get("/posts")
async def get_posts():
    return posts_ref.order_by_child("timestamp").get()
