import requests

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books_by_genre(genre, max_results=10):
    params = {
        "q": f"subject:{genre}",
        "maxResults": max_results,
        "printType": "books",
        "langRestrict": "en"
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return parse_books(resp.json())

def search_books_by_author(author, max_results=10):
    params = {
        "q": f"inauthor:{author}",
        "maxResults": max_results,
        "printType": "books",
        "langRestrict": "en"
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return parse_books(resp.json())

def parse_books(data):
    results = []
    items = data.get("items", [])
    for item in items:
        info = item.get("volumeInfo", {})
        results.append({
            "book_id": item.get("id"),
            "title": info.get("title"),
            "authors": info.get("authors", []),
            "description": info.get("description", ""),
            "categories": info.get("categories", []),
            "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
            "average_rating": info.get("averageRating")
        })
    return results
