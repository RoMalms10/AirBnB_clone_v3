#!/usr/bin/python3
'''
    Implementation of the State class.
'''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os
import models
from models.city import City


class State(BaseModel, Base):
    '''
    State Class.
    Inherits from BaseModel for methods.
    Inherits from Base for use with DB storage when needed.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. The name of the table
        created in MySQL will be called states.
    For Database Storage:
        states Table columns:
            name: String, and can't be NULL.
        cities relationship:
            Linked to the City class.
    For File Storage:
        Attributes:
            name: String
        Methods:
            cities: Getter for cities linked to the current State.
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="delete")
    else:
        name = ""

        @property
        def cities(self):
            '''
                Getter for cities when using FileStorage system
                Returns:
                    A list of City objects associated with the current State
            '''
            city_dict = models.storage.all(City)
            state_query = self.id
            city_list = []
            for k, v in city_dict.items():
                if v.state_id == self.id:
                    city_list.append(v)
            return city_list
