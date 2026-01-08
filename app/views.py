from flask import Blueprint, request, jsonify
from app import app, db
from app.models import Library, Book
from datetime import datetime

# Library Section
@app.route("/libraries", methods=["POST"])
def create_library():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing required fields"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_library = Library(
        name=data["name"],
    )

    db.session.add(new_library)
    db.session.commit()

    return jsonify({
        "id": new_library.id,
        "name": new_library.name
    }), 201

@app.route("/libraries", methods=["GET"])
def list_libraries():

    libraries = Library.query.all()

    return jsonify(
        [
            {
                "id": library.id,
                "name": library.name
            } for library in libraries
        ]
    )

@app.route("/libraries/<int:id>", methods=["PUT"])
def update_library(id):
    library = Library.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        library.name = data["name"]

    db.session.commit()

    return jsonify({
        "id": library.id,
        "name": library.name,
    })

@app.route("/libraries/<int:id>", methods=["DELETE"])
def delete_library(id):
    library = Library.query.get_or_404(id)

    db.session.delete(Library)
    db.session.commit()

    return jsonify({"message": "Library deleted"})


# Book section
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    required = ["title", "author", "library_id"]
    if not data:
        return jsonify({"error": "Missing required fields"}), 400
    for info in required:
        if info not in data:
            return jsonify({"error": "Missing required fields"}), 400

    Library.query.get_or_404(data["library_id"])

    new_book = Book(
        title=data["title"],
        author=data["author"],
        library_id=data["library_id"],
        created_at=datetime.now()
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "library_id": new_book.library_id
    }), 201

@app.route("/books", methods=["GET"])
def list_books():
    query = Book.query

    library_id = request.args.get("library_id")
    search = request.args.get("search")

    if library_id:
        query = query.filter(Book.library_id == library_id)

    if search:
        query = query.filter(
            db.or_(
                        Book.title.ilike(f"%{search}%"),
                        Book.author.ilike(f"%{search}%")
                    )
        )

    books = query.all()

    return jsonify(
        [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "library_id": book.library_id,
                "created_at": book.created_at.isoformat()
            } for book in books
        ]
    )

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]
    if "library_id" in data:
        Library.query.get_or_404(data["library_id"])
        book.library_id = data["library_id"]

    db.session.commit()

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "library_id": book.library_id
    })

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get_or_404(id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"})


