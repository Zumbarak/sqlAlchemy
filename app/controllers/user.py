from app import db
from app.models import User, Library, Book


def create_user(data):
    if not data or "name" not in data:
        raise ValueError("Missing name in request")

    user = User(name=data["name"])
    library = Library(name=f"{data['name']}'s Library", user=user)

    db.session.add(user)
    db.session.add(library)
    db.session.commit()

    return user, library


def get_users():
    return User.query.all()


def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise LookupError("User not found")
    return user


def update_user(user, data):
    if not data or "name" not in data:
        raise ValueError("Missing name in request")

    user.name = data["name"]
    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()


def get_user_book_count(user):
    if not user.library:
        raise LookupError("User does not have a library")

    return Book.query.filter_by(library_id=user.library.id).count()
