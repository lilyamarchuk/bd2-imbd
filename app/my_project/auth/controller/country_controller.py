from my_project.auth.controller.base_controller import BaseController, dto_list
from my_project.auth.service.country_service import CountryService


class CountryController(BaseController):
    def __init__(self):
        super().__init__(CountryService())

    def get_movies(self, item_id):
        return dto_list(self.service.get_movies(item_id))

    def get_box_office(self, item_id):
        return dto_list(self.service.get_box_office(item_id))
