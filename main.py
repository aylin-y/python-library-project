# main.py (async update)
import asyncio
from library import Library

MENU = """
--- Library CLI ---
1) Add Book by ISBN (from Open Library)
2) Remove Book
3) List Books
4) Find Book
5) Exit
"""

async def main():
    lib = Library()

    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            isbn = input("Enter ISBN: ").strip()
            success = await lib.add_book_by_isbn(isbn)
            if success:
                print("✅ Book added from Open Library.")
            else:
                print("⚠️  Could not add book (invalid ISBN or not found).")

        elif choice == "2":
            isbn = input("ISBN to remove: ").strip()
            removed = lib.remove_book(isbn)
            print("✅ Book removed." if removed else "ℹ️  No book found with that ISBN.")

        elif choice == "3":
            books = lib.list_books()
            if not books:
                print("No books in the library yet.")
            else:
                print("--- Books ---")
                for b in books:
                    print(f"- {b}")

        elif choice == "4":
            isbn = input("ISBN to find: ").strip()
            book = lib.find_book(isbn)
            print(book if book else "No book found with that ISBN.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    asyncio.run(main())
