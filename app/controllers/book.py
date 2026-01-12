from flask import request, jsonify
from datetime import datetime
from app import db
from app.models import Book, Library


def create_book():
    data = request.get_json()
    required = ["title", "author", "library_id"]

    if not data or any(field not in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    Library.query.get_or_404(data["library_id"])

    book = Book(
        title=data["title"],
        author=data["author"],
        library_id=data["library_id"],
        created_at=datetime.now(),
    )

    db.session.add(book)
    db.session.commit()

    return (
        jsonify(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "library_id": book.library_id,
            }
        ),
        201,
    )


def list_books():
    query = Book.query

    library_id = request.args.get("library_id")
    search = request.args.get("search")

    if library_id:
        query = query.filter(Book.library_id == library_id)

    if search:
        query = query.filter(
            db.or_(Book.title.ilike(f"%{search}%"), Book.author.ilike(f"%{search}%"))
        )

    books = query.all()

    return jsonify(
        [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "library_id": book.library_id,
                "created_at": book.created_at.isoformat(),
            }
            for book in books
        ]
    )


def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if data:
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        if "library_id" in data:
            Library.query.get_or_404(data["library_id"])
            book.library_id = data["library_id"]

    db.session.commit()

    return jsonify(
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "library_id": book.library_id,
        }
    )


def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"})


def transfer_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if not data or "new_library_id" not in data:
        return jsonify({"error": "Missing new_library_id in request body"}), 400

    new_library_id = data["new_library_id"]
    library = Library.query.get_or_404(new_library_id)

    book.library_id = new_library_id
    db.session.commit()

    return jsonify(
        {"message": f"Book {book.title} transferred to library {library.name}"}
    )
