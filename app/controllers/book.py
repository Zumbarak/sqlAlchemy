from datetime import datetime
from app import db
from app.models import Book, Library


def create_book(data):
    required = ["title", "author", "library_id"]

    if not data or any(field not in data for field in required):
        raise ValueError("Missing required fields")

    library = Library.query.get(data["library_id"])
    if not library:
        raise LookupError("Library not found")

    book = Book(
        title=data["title"],
        author=data["author"],
        library_id=data["library_id"],
        created_at=datetime.now(),
    )

    db.session.add(book)
    db.session.commit()

    return book


def list_books(filters=None):
    query = Book.query

    if filters:
        if "library_id" in filters:
            query = query.filter(Book.library_id == filters["library_id"])

        if "search" in filters:
            search = filters["search"]
            query = query.filter(
                db.or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                )
            )

    return query.all()


def update_book(book, data):
    if "title" in data:
        book.title = data["title"]

    if "author" in data:
        book.author = data["author"]

    if "library_id" in data:
        library = Library.query.get(data["library_id"])
        if not library:
            raise LookupError("Library not found")
        book.library_id = data["library_id"]

    db.session.commit()
    return book


def delete_book(book):
    db.session.delete(book)
    db.session.commit()


def transfer_book(book, data):
    if not data or "new_library_id" not in data:
        raise ValueError("Missing new_library_id")
    new_library_id = data["new_library_id"]
    library = Library.query.get_or_404(new_library_id)
    if not library:
        raise LookupError("Library not found")

    book.library_id = new_library_id
    db.session.commit()
    return library
