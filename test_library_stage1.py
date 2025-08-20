# test_library_stage1.py
# pytest ile çalıştır:  pytest -q
import json
from book import Book
from library import Library

def test_add_and_list_books(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))
    lib.add_book(Book("Dune", "Frank Herbert", "9780441172719"))
    lib.add_book(Book("Neuromancer", "William Gibson", "9780441569595"))

    books = lib.list_books()
    assert len(books) == 2
    assert books[0].isbn == "9780441172719"
    assert books[1].title == "Neuromancer"

def test_find_book(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))
    dune = Book("Dune", "Frank Herbert", "9780441172719")
    lib.add_book(dune)

    found = lib.find_book("9780441172719")
    assert str(found) == str(dune)

def test_remove_book(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))
    lib.add_book(Book("Dune", "Frank Herbert", "9780441172719"))
    lib.add_book(Book("Neuromancer", "William Gibson", "9780441569595"))

    assert lib.remove_book("9780441172719") is True
    assert lib.find_book("9780441172719") is None
    assert lib.remove_book("does-not-exist") is False

def test_persistence_roundtrip(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))
    lib.add_book(Book("Dune", "Frank Herbert", "9780441172719"))

    # reload from disk
    lib2 = Library(filename=str(f))
    assert lib2.find_book("9780441172719") is not None

def test_upsert_on_same_isbn(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))
    lib.add_book(Book("Dune", "Frank Herbert", "9780441172719"))
    lib.add_book(Book("Dune (Updated)", "F. Herbert", "9780441172719"))  # same ISBN

    books = lib.list_books()
    assert len(books) == 1
    assert books[0].title.startswith("Dune")
    # confirm JSON shape
    data = json.loads(f.read_text(encoding="utf-8"))
    assert isinstance(data, list) and "isbn" in data[0]
