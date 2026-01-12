from flask import request, jsonify
from app import db
from app.models import Library


def create_library():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    library = Library(name=data["name"])
    db.session.add(library)
    db.session.commit()

    return jsonify({"id": library.id, "name": library.name}), 201


def list_libraries():
    libraries = Library.query.all()

    return jsonify([{"id": library.id, "name": library.name} for library in libraries])


def update_library(id):
    library = Library.query.get_or_404(id)
    data = request.get_json()

    if data and "name" in data:
        library.name = data["name"]

    db.session.commit()

    return jsonify({"id": library.id, "name": library.name})


def delete_library(id):
    library = Library.query.get_or_404(id)

    db.session.delete(library)
    db.session.commit()

    return jsonify({"message": "Library deleted"})
