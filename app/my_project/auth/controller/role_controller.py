from my_project.auth.controller.base_controller import BaseController, dto_list
from my_project.auth.service.role_service import RoleService


class RoleController(BaseController):
    def __init__(self):
        super().__init__(RoleService())

    def get_cast(self, item_id):
        return dto_list(self.service.get_cast(item_id))
