from flask import jsonify, request


def dto_list(items):
    return jsonify([i.to_dto() for i in items])


class BaseController:

    def __init__(self, service):
        self.service = service

    def get_all(self):
        return dto_list(self.service.get_all())

    def get_one(self, item_id):
        return jsonify(self.service.get_by_id(item_id).to_dto())

    def create(self):
        obj = self.service.create(request.get_json(silent=True))
        return jsonify(obj.to_dto()), 201

    def update(self, item_id):
        obj = self.service.update(item_id, request.get_json(silent=True))
        return jsonify(obj.to_dto())

    def delete(self, item_id):
        self.service.delete(item_id)
        return jsonify({"message": f"{self.service.label} з id={item_id} видалено"})
