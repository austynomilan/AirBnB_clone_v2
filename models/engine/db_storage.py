#!/usr/bin/python3
import os
from models.base_model import Base
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Database engine"""
    __engine = None
    __session = None

    def __init__(self):
        """intializing"""

        mysql_user = os.environ.get('HBNB_MYSQL_USER')
        mysql_password = os.environ.get('HBNB_MYSQL_PWD')
        mysql_host = os.environ.get('HBNB_MYSQL_HOST')
        mysql_db = os.environ.get('HBNB_MYSQL_DB')

        connection = 'mysql+mysqldb://{}:{}@{}/{}'\
            .format(mysql_user, mysql_password, mysql_host, mysql_db)

        self.__engine = create_engine(connection, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)

        check_environ = os.environ.get('HBNB_ENV')
        if check_environ == 'test':
            Base.metadata.drop_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        """Query all objects based on the class name"""
        objects = {}
        objects_dict = {}
        cls_to_query = {
            'Amenity': Amenity,
            'City': City,
            'Place': Place,
            'State': State,
            'Review': Review,
            'User': User
        }

        if cls is not None:
            cls = cls_to_query.get(cls, None)
            objects = self.__session.query(cls).all()
        else:
            cls_to_query = [User, State, City, Amenity, Place, Review]
            objects = []

            for cls in cls_to_query:
                objects.extend(self.__session.query(cls).all())

        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if obj._sa_instance_state is not None:
                del obj._sa_instance_state
            objects_dict[key] = obj

        return objects_dict

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Load tables in the database"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                    }
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self._session = Session()
