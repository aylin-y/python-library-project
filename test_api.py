# test_api.py
import pytest
from fastapi.testclient import TestClient
from api import app
from library import Library

client = TestClient(app)


def test_get_books_initially_empty(tmp_path, monkeypatch):
    # monkeypatch library instance to use temp file
    lib = Library(filename=str(tmp_path / "lib.json"))
    monkeypatch.setattr("api.library", lib)

    resp = client.get("/books")
    assert resp.status_code == 200
    assert resp.json() == []


def test_post_and_get_book(tmp_path, monkeypatch):
    lib = Library(filename=str(tmp_path / "lib.json"))
    monkeypatch.setattr("api.library", lib)

    # Add book by ISBN (Dune example)
    resp = client.post("/books", json={"isbn": "9780441172719"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["isbn"] == "9780441172719"
    assert "Dune" in data["title"]

    # Now GET /books should return it
    resp2 = client.get("/books")
    books = resp2.json()
    assert any(b["isbn"] == "9780441172719" for b in books)


def test_delete_book(tmp_path, monkeypatch):
    lib = Library(filename=str(tmp_path / "lib.json"))
    monkeypatch.setattr("api.library", lib)

    # Add first
    client.post("/books", json={"isbn": "9780441172719"})

    # Delete
    resp = client.delete("/books/9780441172719")
    assert resp.status_code == 200
    assert resp.json() == {"detail": "Book removed"}

    # Verify empty
    resp2 = client.get("/books")
    assert resp2.json() == []
