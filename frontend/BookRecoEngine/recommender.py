from typing import List, Dict
from collections import Counter
from db import get_user
from google_books import search_books_by_genre, search_books_by_author

def get_user_profile(user_id: str):
    user = get_user(user_id)
    if not user:
        return {
            "preferred_genres": [],
            "preferred_authors": []
        }
    genres = user.get("preferred_genres", [])
    authors = user.get("preferred_authors", [])

    ratings = user.get("ratings", [])
    genre_counts = Counter()
    for r in ratings:
        for g in r.get("genres", []):
            if r.get("rating", 0) >= 4:
                genre_counts[g] += 1

    top_genres_from_ratings = [g for g, _ in genre_counts.most_common(3)]
    all_genres = list(dict.fromkeys(genres + top_genres_from_ratings))

    return {
        "preferred_genres": all_genres,
        "preferred_authors": authors
    }

def get_personalized_recommendations(user_id: str, max_results_per_query: int = 5) -> List[Dict]:
    profile = get_user_profile(user_id)
    genres = profile["preferred_genres"]
    authors = profile["preferred_authors"]

    books = []
    seen_ids = set()

    for g in genres:
        for book in search_books_by_genre(g, max_results=max_results_per_query):
            if book["book_id"] not in seen_ids:
                seen_ids.add(book["book_id"])
                books.append(book)

    for a in authors:
        for book in search_books_by_author(a, max_results=max_results_per_query):
            if book["book_id"] not in seen_ids:
                seen_ids.add(book["book_id"])
                books.append(book)

    return books
