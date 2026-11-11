from my_project.utils.errors import ApiError


class BaseService:
    dao = None
    label = "Запис"
    required = ()

    def get_all(self):
        return self.dao.find_all()

    def get_by_id(self, item_id):
        obj = self.dao.find_by_id(item_id)
        if obj is None:
            raise ApiError(f"{self.label} з id={item_id} не знайдено", 404)
        return obj

    def create(self, data):
        self._check_body(data)
        missing = [f for f in self.required if data.get(f) in (None, "")]
        if missing:
            raise ApiError(f"Відсутні обов'язкові поля: {', '.join(missing)}", 400)
        data = self.prepare(data)
        self.validate(data)
        return self.dao.create(data)

    def update(self, item_id, data):
        self._check_body(data)
        obj = self.get_by_id(item_id)
        empty = [f for f in self.required if f in data and data[f] in (None, "")]
        if empty:
            raise ApiError(f"Поля не можуть бути порожніми: {', '.join(empty)}", 400)
        self.validate(data)
        return self.dao.update(obj, data)

    def delete(self, item_id):
        self.dao.delete(self.get_by_id(item_id))

    def prepare(self, data):
        return data

    def validate(self, data):
        pass

    @staticmethod
    def _check_body(data):
        if not isinstance(data, dict) or not data:
            raise ApiError("Тіло запиту має бути непорожнім JSON-об'єктом", 400)
