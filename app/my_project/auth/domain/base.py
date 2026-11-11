from datetime import date, datetime
from decimal import Decimal

from my_project.utils.db import db


class BaseModel(db.Model):
    __abstract__ = True
    __writable__ = ()

    def to_dto(self):
        dto = {}
        for col in self.__table__.columns:
            value = getattr(self, col.key)
            if isinstance(value, (date, datetime)):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            dto[col.key] = value
        return dto

    def update_from(self, data):
        for field in self.__writable__:
            if field in data:
                setattr(self, field, data[field])
