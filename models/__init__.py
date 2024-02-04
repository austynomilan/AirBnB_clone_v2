#!/usr/bin/python3
"""Changing storage type using env variable"""
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
import os

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    Storage = DBStorage()
    Storage.reload()
else:
    Storage = FileStorage()
    Storage.reload()

__all__ = ['BaseModel', 'User',
           'Place', 'City', 'State',
           'Amenity', 'Review', 'Storage']
