# book.py  (kod bloğu olarak veriyorum; dosyaya ayırmadan kopyalayıp kullanabilirsin)
from typing import Dict, Any

class Book:
    """
    Represents a single book entity.
    Invariants:
      - title, author, isbn are non-empty strings.
    """

    def __init__(self, title: str, author: str, isbn: str):
        title = (title or "").strip()
        author = (author or "").strip()
        isbn = (isbn or "").strip()

        if not title:
            raise ValueError("title must not be empty")
        if not author:
            raise ValueError("author must not be empty")
        if not isbn:
            raise ValueError("isbn must not be empty")

        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        return cls(title=data["title"], author=data["author"], isbn=data["isbn"])
