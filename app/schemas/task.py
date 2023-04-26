from sqlalchemy import Column, String, Integer, Enum, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity, Base, TaskStatus


class Task(Base, BaseEntity):
    __tablename__ = "task"

    user_id = Column(Uuid, ForeignKey('users.id'))
    summary = Column(String(50))
    description = Column(String(255))
    status = Column(Enum(TaskStatus))
    priority = Column(Integer)

    user = relationship("User")
