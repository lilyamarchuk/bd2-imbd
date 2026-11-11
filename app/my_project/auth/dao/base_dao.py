from my_project.utils.db import db


class BaseDAO:
    model = None

    def find_all(self):
        return self.model.query.all()

    def find_by_id(self, item_id):
        return db.session.get(self.model, item_id)

    def create(self, data):
        obj = self.model(**{f: data[f] for f in self.model.__writable__ if f in data})
        db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, obj, data):
        obj.update_from(data)
        db.session.commit()
        return obj

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
