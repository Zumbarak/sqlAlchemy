from flask import Blueprint, request, jsonify
from app.controllers.book import (
    create_book,
    list_books,
    update_book,
    delete_book,
    transfer_book,
)
from app.models import Book

bp = Blueprint("books", __name__)


@bp.route("/books", methods=["POST"])
def create_book_route():
    try:
        book = create_book(request.get_json())
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
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/books", methods=["GET"])
def list_books_route():
    filters = {
        "library_id": request.args.get("library_id"),
        "search": request.args.get("search"),
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    books = list_books(filters)
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


@bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book_route(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    try:
        book = update_book(book, data)
        return jsonify(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "library_id": book.library_id,
            }
        )
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_route(book_id):
    book = Book.query.get_or_404(book_id)
    delete_book(book)
    return jsonify({"message": "Book deleted"})


@bp.route("/books/<int:book_id>/transfer", methods=["POST"])
def transfer_book_route(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    if not data or "new_library_id" not in data:
        return jsonify({"error": "Missing new_library_id in request body"}), 400
    try:
        library = transfer_book(book, data)
        return jsonify(
            {"message": f"Book {book.title} transferred to library {library.name}"}
        )
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
