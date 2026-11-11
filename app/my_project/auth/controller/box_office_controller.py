from my_project.auth.controller.base_controller import BaseController
from my_project.auth.service.box_office_service import BoxOfficeService


class BoxOfficeController(BaseController):
    def __init__(self):
        super().__init__(BoxOfficeService())
