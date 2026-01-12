from flask import request, jsonify
from app import db
from app.models import User, Library, Book


def create_user():
    data = request.get_json()
    if not data or not "name" in data:
        return jsonify({"error": "Missing name in request"}), 400

    user = User(name=data["name"])
    library = Library(name=f"{data['name']}'s Library", user=user)

    db.session.add(user)
    db.session.add(library)
    db.session.commit()

    return jsonify({"id": user.id, "name": user.name, "library_id": library.id}), 201


def get_users():
    users = User.query.all()
    return jsonify(
        [
            {
                "id": user.id,
                "name": user.name,
                "library_id": user.library.id if user.library else None,
            }
            for user in users
        ]
    )


def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(
        {
            "id": user.id,
            "name": user.name,
            "library_id": user.library.id if user.library else None,
        }
    )


def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data or not "name" in data:
        return jsonify({"error": "Missing name in request"}), 400

    user.name = data["name"]
    db.session.commit()

    return jsonify({"id": user.id, "name": user.name})


def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


def get_user_book_count(user_id):
    user = User.query.get_or_404(user_id)
    if not user.library:
        return jsonify({"error": "User does not have a library"}), 404

    book_count = Book.query.filter_by(library_id=user.library.id).count()
    return jsonify({"book_count": book_count})
