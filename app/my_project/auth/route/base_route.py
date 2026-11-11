from flask import Blueprint


def create_crud_blueprint(name, prefix, controller):
    bp = Blueprint(name, __name__, url_prefix=prefix)
    bp.add_url_rule("", "get_all", controller.get_all, methods=["GET"])
    bp.add_url_rule("", "create", controller.create, methods=["POST"])
    bp.add_url_rule("/<int:item_id>", "get_one", controller.get_one, methods=["GET"])
    bp.add_url_rule("/<int:item_id>", "update", controller.update, methods=["PUT"])
    bp.add_url_rule("/<int:item_id>", "delete", controller.delete, methods=["DELETE"])
    return bp
