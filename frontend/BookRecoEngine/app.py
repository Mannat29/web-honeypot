from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from db import get_user, upsert_user, add_rating
from google_books import search_books_by_genre, search_books_by_author
from recommender import get_personalized_recommendations

# For auto-opening page
import webbrowser
import threading

app = FastAPI(title="Book Recommendation Engine")

# Allow browser frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# MODELS
# ------------------------------

class UserPrefs(BaseModel):
    name: Optional[str] = None
    preferred_genres: List[str] = []
    preferred_authors: List[str] = []


class Rating(BaseModel):
    book_id: str
    title: str
    authors: List[str]
    rating: int
    genres: List[str] = []


# ------------------------------
# FRONTEND ROUTE (NEW UI)
# ------------------------------

@app.get("/", include_in_schema=False)
def root_page():
    # serve index.html from the same folder as app.py
    return FileResponse("index.html")


# ------------------------------
# API ROUTES
# ------------------------------

@app.post("/user/{user_id}/preferences")
def set_preferences(user_id: str, prefs: UserPrefs):
    existing = get_user(user_id) or {}
    data = {
        "name": prefs.name or existing.get("name"),
        "preferred_genres": prefs.preferred_genres or existing.get("preferred_genres", []),
        "preferred_authors": prefs.preferred_authors or existing.get("preferred_authors", []),
    }
    upsert_user(user_id, data)
    return {"status": "ok", "user": data}


@app.post("/user/{user_id}/ratings")
def add_user_rating(user_id: str, rating: Rating):
    add_rating(user_id, rating.dict())
    return {"status": "ok"}


@app.get("/search/genre/{genre}")
def recommend_by_genre(genre: str):
    books = search_books_by_genre(genre)
    return {"genre": genre, "books": books}


@app.get("/search/author/{author}")
def recommend_by_author(author: str):
    books = search_books_by_author(author)
    return {"author": author, "books": books}


@app.get("/user/{user_id}/recommendations")
def personalized_recommendations(user_id: str):
    books = get_personalized_recommendations(user_id)
    return {"user_id": user_id, "books": books}


# ------------------------------
# AUTO OPEN BROWSER
# ------------------------------

def open_browser():
    # open the NEW UI, not /docs
    webbrowser.open("http://127.0.0.1:8000/")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
