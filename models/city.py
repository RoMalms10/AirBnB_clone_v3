#!/usr/bin/python3
'''
    Implementation of the City class.
'''
import os
from models import storage, classes
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    '''
    City Class.
    Inherits from BaseModel for methods.
    Inherits from Base for use with DB storage when needed.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. The name of the table
        created in MySQL will be called cities.
    For Database Storage:
        cities Table columns:
            name: String, and can't be NULL
            state_id: String, can't be NULL and links to
                another table called states based off it's id.
        places relationship:
            Linked to the Place class.
    For File Storage:
        Attributes:
            name: String
            state_id: String
        Methods:
            places: Getter for places linked to the current City.
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "cities"

        __mapper_args__ = {
            'confirm_deleted_rows': False}

        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="delete")
    else:
        name = ""
        state_id = ""

        @property
        def places(self):
            '''
                Getter for places when using FileStorage system
                Returns:
                    A list of Place objects associated with the current City
            '''
            cls_dict = storage.all(classes["Place"])
            places_in_city = []
            current_city = self.id
            for key, value in cls_dict.items():
                if value.city_id == current_city:
                    places_in_city.append(value)
            return places_in_city
