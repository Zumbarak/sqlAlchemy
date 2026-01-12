from app.controllers.book import (
    create_book,
    list_books,
    update_book,
    delete_book,
    transfer_book,
)


def register_book_routes(app):
    app.route("/books", methods=["POST"])(create_book)
    app.route("/books", methods=["GET"])(list_books)
    app.route("/books/<int:book_id>", methods=["PUT"])(update_book)
    app.route("/books/<int:book_id>", methods=["DELETE"])(delete_book)
    app.route("/books/<int:book_id>/transfer", methods=["POST"])(transfer_book)
