from flask import request, jsonify

from my_project.auth.controller.base_controller import BaseController, dto_list
from my_project.auth.service.person_service import PersonService


class PersonController(BaseController):
    def __init__(self):
        super().__init__(PersonService())

    def get_all(self):
        return dto_list(self.service.get_all(name=request.args.get("name")))

    def get_filmography(self, item_id):
        return dto_list(self.service.get_filmography(item_id))
