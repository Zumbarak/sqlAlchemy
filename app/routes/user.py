from app.controllers.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
    get_user_book_count,
)


def register_user_routes(app):
    app.route("/users", methods=["POST"])(create_user)
    app.route("/users", methods=["GET"])(get_users)
    app.route("/users/<int:user_id>", methods=["GET"])(get_user)
    app.route("/users/<int:user_id>", methods=["PUT"])(update_user)
    app.route("/users/<int:user_id>", methods=["DELETE"])(delete_user)
    app.route("/users/<int:user_id>/book_count", methods=["GET"])(get_user_book_count)
