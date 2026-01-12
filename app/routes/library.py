from app.controllers.library import (
    create_library,
    list_libraries,
    update_library,
    delete_library,
)


def register_library_routes(app):
    app.route("/libraries", methods=["POST"])(create_library)
    app.route("/libraries", methods=["GET"])(list_libraries)
    app.route("/libraries/<int:id>", methods=["PUT"])(update_library)
    app.route("/libraries/<int:id>", methods=["DELETE"])(delete_library)
