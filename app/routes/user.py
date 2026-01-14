from flask import Blueprint, request, jsonify
from app.controllers.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_book_count,
)
from app.models import User

bp = Blueprint("users", __name__)


@bp.route("/users", methods=["POST"])
def create_user_route():
    try:
        user, library = create_user(request.get_json())
        return jsonify({"user_id": user.id, "user_name": user.name, "library_id": library.id, "library_name": library.name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/users", methods=["GET"])
def list_users_route():
    users = get_users()
    return jsonify([{"id": u.id, "name": u.name} for u in users])


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    try:
        user = get_user(user_id)
        return jsonify({"id": user.id, "name": user.name})
    except LookupError as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    user = User.query.get_or_404(user_id)
    try:
        user = update_user(user, request.get_json())
        return jsonify({"id": user.id, "name": user.name})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    user = User.query.get_or_404(user_id)
    delete_user(user)
    return jsonify({"message": "User deleted"})


@bp.route("/users/<int:user_id>/books/count", methods=["GET"])
def get_user_book_count_route(user_id):
    user = User.query.get_or_404(user_id)
    try:
        count = get_user_book_count(user)
        return jsonify({"book_count": count})
    except LookupError as e:
        return jsonify({"error": str(e)}), 404