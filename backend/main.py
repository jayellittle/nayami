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
    ETC = "etc"
    STUDY = "study"
    WORK = "work"
    RELATIONSHIP = "relationship"
    LOVE = "love"

class Post(BaseModel):
    title: str
    body: str
    categories: List[CategoryEnum]
    hashtags: List[str]

class SortField(str, Enum):
    TIMESTAMP = "timestamp"
    TITLE = "title"
    CATEGORY = "category"

class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"

@app.post("/posts")
async def create_post(post: Post):
    cleaned_hashtags = [
        tag.lower().strip().replace('#', '')
        for tag in post.hashtags
    ]

    new_post = {
        "title": post.title,
        "body": post.body,
        "categories": [cat.value for cat in post.categories],
        "hashtags": cleaned_hashtags,
        "timestamp": {'.sv': 'timestamp'}
    }
    posts_ref.push(new_post)
    return {"status": "success"}


@app.get("/posts")
async def get_posts(
    hashtag: str | None = None,
    category: CategoryEnum | None = None,
    sort_by: SortField | None = SortField.TIMESTAMP,
    direction: SortDirection | None = SortDirection.DESC
):
    results = posts_ref.order_by_child(sort_by.value).get()

    if results:
        posts = dict(results)

        # Filter by category if specified
        if category:
            posts = {
                k: v for k, v in posts.items() 
                if category.value in v.get('categories', [])
            }
        
        # Filter by hashtag if specified
        if hashtag:
            clean_hashtag = hashtag.lower().strip().replace('#', '')
            posts = {
                k: v for k, v in posts.items()
                if clean_hashtag in v.get('hashtags', [])
            }

        # Apply sorting
        if direction == SortDirection.ASC:
            posts = dict(sorted(posts.items()))
        else:
            posts = dict(sorted(posts.items(), reverse=True))
        return posts
        
    return {}
