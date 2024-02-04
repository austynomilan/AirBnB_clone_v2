#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    storage = os.environ.get('HBNB_TYPE_STORAGE')
    if storage == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
                "City",
                backref="state",
                cascade="all,  delete-orphan")
    else:
        name = ""

    @property
    def cities(self):
        """Getter attribute for FileStorage"""
        from models import storage
        from models import City
        lists = []
        for val in storage.all(City).values():
            if self.id == val.state_id:
                lists.append(val)
        return lists
