#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

if storage_type.lower() == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
