from app import db
from app.models import Library


def create_library(data):
    if not data or "name" not in data:
        raise ValueError("Missing required fields")

    library = Library(name=data["name"])
    db.session.add(library)
    db.session.commit()

    return library


def list_libraries():
    return Library.query.all()


def update_library(library, data):
    if data and "name" in data:
        library.name = data["name"]

    db.session.commit()
    return library


def delete_library(library):
    db.session.delete(library)
    db.session.commit()
