# test_library_stage2.py
import pytest
import asyncio
from library import Library

# pytest-asyncio marker allows async test functions
@pytest.mark.asyncio
async def test_add_book_by_isbn_success(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))

    # known ISBN: Dune (Frank Herbert)
    isbn = "9780441172719"
    success = await lib.add_book_by_isbn(isbn)

    assert success is True
    book = lib.find_book(isbn)
    assert book is not None
    assert "Dune" in book.title

@pytest.mark.asyncio
async def test_add_book_by_isbn_not_found(tmp_path):
    f = tmp_path / "lib.json"
    lib = Library(filename=str(f))

    isbn = "0000000000000"  # nonsense ISBN
    success = await lib.add_book_by_isbn(isbn)

    assert success is False
    assert lib.find_book(isbn) is None
