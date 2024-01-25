#!/usr/bin/python3
'''The db storage for the hbnb project'''
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User

class DBStorage:
    """Data storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB'),
            pool_pre_ping=True
	))
   

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self._engine)

    def new(self, obj):
        """Add the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all the changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and the current database session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self._session = Session()
        
        State.cities = relationship("City", cascade="all, delete-orphan", backref="state")

    def all(self, cls=None):
        """Query all objects based on the class name or all objects if cls=None."""
        classes = {
            "City": City,
            "State": State,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity
        }
       
        result = {}
        query_rows = []

        if cls:
            """Query for all objects belonging to cls"""
            if type(cls) is str:
                cls = eval(cls)
            query_rows = self.__session.query(cls)
            for obj in query_rows:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                result[key] = obj
            return result

        else:
            """Query for all types of object"""
            for name, value in classes.items():
                query_rows = self.__session.query(value)
                for obj in query_rows:
                    key = '{}.{}'.format(name, obj.id)
                    result[key] = obj
            return result
	    
    def close(self):
        """Because SQLAlchemy doesn't reload his `Session`
        when it's time to insert new data, we force it to!"""
        self.__session.close()
