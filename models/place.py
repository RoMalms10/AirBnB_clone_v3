#!/usr/bin/python3
'''
    Implementation of the Place class.
    For Data Storage:
        Define an association table called place_amenity. This table links
            places and amenities based on their id's.
'''
import os
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, Float, Table

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    association_table = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60), ForeignKey(
                                  'places.id'), nullable=False),
                              Column('amenity_id', String(60), ForeignKey(
                                  'amenities.id'), nullable=False)
                              )


class Place(BaseModel, Base):
    '''
    Place Class.
    Inherits from BaseModel for methods.
    Inherits from Base for use with DB storage when needed.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. The name of the table
        created in MySQL will be called places.
    For Database Storage:
        places Table columns:
            city_id: String, can't be NULL, and links to
                another table called cities based off it's id.
            user_id: String, can't be NULL and links to
                another table called users based off it's id.
            name: String, and can't be NULL.
            description: String, and can be NULL.
            number_rooms: Integer, default value of 0,
                and can't be NULL.
            number_bathrooms: Integer, default value of 0,
                and can't be NULL.
            max_guest: Integer, default value of 0,
                and can't be NULL.
            price_by_night: Integer, default value of 0,
                and can't be NULL.
            latitude: Float, and can be NULL.
            longitude: Float, and can be NULL.
        reviews relationship:
            Linked to the Review class.
        amenities relationship:
            Linked to the Amenity class.
        amenity_ids: list of amenity objects associated with this Place.
    For File Storage:
        Attributes:
            city_id: String
            user_id: String
            name: String
            description: String
            number_rooms: Integer, default of 0
            number_bathrooms: Integer, default of 0
            max_guest: Integer, default of 0
            price_by_night: Integer, default of 0
            latitude: Float, default 0.0
            longitude: Float, default 0.0
            amenity_ids: list of amenity ids associated with this Place.
        Methods:
            amenities: Getter for amenity ids linked to the current Place.
            amenities: Setter for adding amenity ids to the current Place.
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)
        amenity_ids = []
        reviews = relationship("Review", cascade="delete", backref="place")
        amenities = relationship("Amenity",
                                 secondary=association_table,
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            '''
            Returns:
                List containing Amenity ids linked to this Place.
            '''
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            '''
            Adds Amenity ids to the amenity_ids list.
            Returns:
                Nothing
            '''
            self.amenity_ids = obj.id
            if obj.__class__.__name__ != "Amenity":
                return
            amenity_dict = models.storage.all(obj)
            place_id = self.id
            for key, val in amenity_dict.items():
                if self.id == val.place_id:
                    self.amenity_ids.append(val.id)
