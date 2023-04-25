from sqlalchemy import Column, Uuid, Time
from sqlalchemy.ext.declarative import declarative_base
import enum
import uuid


class Gender(enum.Enum):
    NONE = 'N'
    FEMALE = 'F'
    MALE = 'M'


class TaskStatus(enum.Enum):
    DONE = 'Done'
    DOING = 'Doing'
    CLOSED = 'Closed'
    OPEN = 'Open'
    PENDING = 'Pending'


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False)
    updated_at = Column(Time, nullable=False)


Base = declarative_base()
