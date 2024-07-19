from datetime import datetime

from sqlalchemy import DateTime, Column, func, event
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime(timezone=True),  server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    @classmethod
    def __declare_last__(cls):
        @event.listens_for(cls, 'before_update', propagate=True)
        def receive_before_update(mapper, connection, target):
            target.updated_at = datetime.now()


class BaseModel(Base, TimestampMixin):
    __abstract__ = True
