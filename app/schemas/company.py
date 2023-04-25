import uuid
from sqlalchemy import Column, String, Boolean, Float
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity, Base


class Company(Base, BaseEntity):
    __tablename__ = "company"

    name = Column(String(50))
    description = Column(String(255))
    mode = Column(Boolean, default=True)
    rating = Column(Float)

    users = relationship("User", back_populates="company")
