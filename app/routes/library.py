from flask import Blueprint, request, jsonify
from app.controllers.library import (
    create_library,
    list_libraries,
    update_library,
    delete_library,
)
from app.models import Library

bp = Blueprint("libraries", __name__)


@bp.route("/libraries", methods=["POST"])
def create_library_route():
    try:
        library = create_library(request.get_json())
        return jsonify({"id": library.id, "name": library.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/libraries", methods=["GET"])
def list_libraries_route():
    libraries = list_libraries()
    return jsonify([{"id": lib.id, "name": lib.name} for lib in libraries])


@bp.route("/libraries/<int:library_id>", methods=["PUT"])
def update_library_route(library_id):
    library = Library.query.get_or_404(library_id)
    library = update_library(library, request.get_json())
    return jsonify({"id": library.id, "name": library.name})


@bp.route("/libraries/<int:library_id>", methods=["DELETE"])
def delete_library_route(library_id):
    library = Library.query.get_or_404(library_id)
    delete_library(library)
    return jsonify({"message": "Library deleted"})
