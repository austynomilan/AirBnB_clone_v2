#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.city import City
from models.user import User
from models.review import Review
import os


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    storage = os.environ.get('HBNB_TYPE_STORAGE')
    if storage == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True, default=0)
        longitude = Column(Float, nullable=True, default=0)
        amenity_ids = []

        reviews = relationship(
            "Review",
            backref="place",
            cascade="all,  delete-orphan")

        place_amenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True, nullable=False)
        )

        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False, backref="places")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0
        longitude = 0
        amenity_ids = []

        @property
        def reviews(self):
            """ getter attribute for reviews """
            from models import storage
            if self.id is not None:
                lists = []
                for val in storage.all(Review).values():
                    if val.place_id == self.id:
                        lists.append(val)
                return lists

        @property
        def amenities(self):
            """ getter attribute for amenities """
            from models import storage
            from models import Amenity
            lists = []
            for val in storage.all(Amenity).values():
                if val.id == self.amenity_ids:
                    lists.append(val)
            return lists

        @amenities.setter
        def amenities(self, amenity):
            """ setter attribute for amenities """
            from models.amenity import Amenity
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)
