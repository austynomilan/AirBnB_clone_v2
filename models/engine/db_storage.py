#!/usr/bin/python3
'''The db storage for the hbnb project'''
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """Data storage engine"""
    def __init__(self):
        self.__engine = None
	self.__session = None
	self.create_engine()

    def create_engine(self):
        """Create the engine and link it to the MySQL database."""
        db_user = os.environ.get('HBNB_MYSQL_USER', 'hbnb_dev')
        db_password = os.environ.get('HBNB_MYSQL_PWD', 'default pwd')
        db_host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        db_name = os.environ.get('HBNB_MYSQL_DB', 'hbnb_dev_db')
        env = os.environ.get('HBNB_ENV', 'production')

	engine_str = f'mysql+mysqldb://{db_user}:{db_password}@{db_host}/{db_name}'
        self.__engine = create_engine(engine_str, pool_pre_ping=True)

        if env == 'test':
            metadata = MetaData(self.__engine)
            metadata.reflect()
            metadata.drop_all()

    def init_session(self):
        """Initiate a session to interact with the database."""
        if self.__engine is not None:
            Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
	    self.__session = scoped_session(Session)
        else:
            print("Error: Engine not created. Call create_engine() first.")

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
        from model.base_model import Base

        Base.metadata.create_all(self.__engine)

        self.init_session()
        
        State.cities = relationship("City", cascade="all, delete-orphan", backref="state")

    def all(self, cls=None):
        """Query all objects based on the class name or all objects if cls=None."""
        from models.base_model import Base
       
        result_dict = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            all_classes = [User, State, City, Amenity, Place, Review]
            objects = []
            for model_class in all_classes:
                objects.extend(self.__session.query(model_class).all())

        for obj in objects:
            key = f"{obj.__class__.__name__}.{obj.id}"
            result_dict[key] = obj
        return result_dict


 
