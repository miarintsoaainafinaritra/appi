from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List
from datetime import datetime
import base64

app = FastAPI()
security = HTTPBasic()


posts_db = []

# Q1: Route GET /ping
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"

# Q2: Route GET /home
@app.get("/home", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Welcome home!</h1>
        </body>
    </html>
    """

# Q3: Gestion des 404
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return HTMLResponse(
        content="<html><body><h1>404 NOT FOUND</h1></body></html>",
        status_code=404
    )


class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

# Q4: Route POST /posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(new_posts: List[Post]):
    posts_db.extend(new_posts)
    return posts_db

# Q5: Route GET /posts
@app.get("/posts")
async def get_posts():
    return posts_db

# Q6: Route PUT /posts
@app.put("/posts")
async def update_or_add_post(post: Post):
    for idx, existing_post in enumerate(posts_db):
        if existing_post.title == post.title:
            posts_db[idx] = post
            return posts_db
    posts_db.append(post)
    return posts_db


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "123456"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/ping/auth", response_class=PlainTextResponse)
async def ping_auth(username: str = Depends(verify_credentials)):
    return "pong"
