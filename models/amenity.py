#!/usr/bin/python3
'''
    Implementation of the Amenity class.
'''
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    '''
    Amenity Class.
    Inherits from BaseModel for methods.
    Inherits from Base for use with DB storage when needed.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. The name of the table
        created in MySQL will be called amenities.
    For Database Storage:
        amenities Table columns:
            name: String, and can't be NULL
    For File Storage:
        Attributes:
            name: String
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""
