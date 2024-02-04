#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models.user import User
import os


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'

    storage = os.environ.get('HBNB_TYPE_STORAGE')
    if storage == 'db':
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        text = ""
        place_id = ""
        user_id = ""
