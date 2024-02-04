#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import Place
import os


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'

    storage = os.environ.get('HBNB_TYPE_STORAGE')
    if storage == 'db':
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
                "Place", secondary=Place.place_amenity,
                overlaps="amenities,places")
    else:
        name = ""
