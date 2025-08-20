# library.py
import json
import os
import httpx
import asyncio
from typing import List, Optional
from book import Book

class Library:
    """
    Library manages the collection of books and persistence to a JSON file.
    """

    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books: List[Book] = []
        self._load_books()

    # ---------- Public API ----------
    def add_book(self, book: Book) -> None:
        """Adds a new book. If same ISBN exists, replace it (upsert semantics)."""
        existing = self.find_book(book.isbn)
        if existing:
            # replace in-place to ensure uniqueness on ISBN
            self._replace(book.isbn, book)
        else:
            self.books.append(book)
        self._save_books()

    def remove_book(self, isbn: str) -> bool:
        """Removes a book by ISBN. Returns True if removed, False otherwise."""
        before = len(self.books)
        self.books = [b for b in self.books if b.isbn != isbn]
        removed = len(self.books) < before
        if removed:
            self._save_books()
        return removed

    def list_books(self) -> List[Book]:
        return list(self.books)

    def find_book(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    # ---------- Internal helpers ----------
    def _replace(self, isbn: str, book: Book) -> None:
        for i, b in enumerate(self.books):
            if b.isbn == isbn:
                self.books[i] = book
                return

    def _load_books(self) -> None:
        if not os.path.exists(self.filename):
            self.books = []
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.books = [Book.from_dict(item) for item in (raw or [])]
        except (json.JSONDecodeError, OSError, KeyError, TypeError) as e:
            # Defensive: if file is corrupted, reset to empty and do not crash.
            print(f"[WARN] Failed to load library data ({e}). Starting with an empty collection.")
            self.books = []

    def _save_books(self) -> None:
        data = [b.to_dict() for b in self.books]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    async def add_book_by_isbn(self, isbn: str) -> bool:
        """
        Asynchronously fetch book details from Open Library by ISBN.
        Returns True if added successfully, False otherwise.
        """
        url = f"https://openlibrary.org/isbn/{isbn}.json"
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    print("⚠️  Book not found in Open Library.")
                    return False

                data = resp.json()
                title = data.get("title")
                authors = data.get("authors", [])

                # Launch concurrent tasks for author fetches
                tasks = []
                for author in authors:
                    author_url = f"https://openlibrary.org{author['key']}.json"
                    tasks.append(client.get(author_url))

                results = await asyncio.gather(*tasks, return_exceptions=True)

                author_names = []
                for r in results:
                    if isinstance(r, Exception):
                        continue
                    if r.status_code == 200:
                        adata = r.json()
                        author_names.append(adata.get("name", "Unknown"))

                author_str = ", ".join(author_names) if author_names else "Unknown Author"

                if not title:
                    print("⚠️  Book data incomplete.")
                    return False

                book = Book(title=title, author=author_str, isbn=isbn)
                self.add_book(book)
                return True

            except httpx.RequestError as e:
                print(f"⚠️  Network error: {e}")
                return False
