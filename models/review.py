#!/usr/bin/python3
'''
    Implementation of the Review class.
'''

import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    '''
    Review Class.
    Inherits from BaseModel for methods.
    Inherits from Base for use with DB storage when needed.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. The name of the table
        created in MySQL will be called reviews.
    For Database Storage:
        reviews Table columns:
            text: String, and can't be NULL
            place_id: String, can't be NULL and links to
                another table called places based off it's id.
            user_id: String, can't be NULL and links to
                another table called users based off it's id.
    For File Storage:
        Attributes:
            text: String
            place_id: String
            user_id: String
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60),  ForeignKey("users.id"), nullable=False)
    else:
        text = ""
        place_id = ""
        user_id = ""
