#!/usr/bin/python3
'''
    Implementation of the User class.
'''
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    '''
    User Class.
    Inherits from BaseModel for methods.
    Inherits from Base for use with DB storage when needed.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. The name of the table
        created in MySQL will be called users.
    For Database Storage:
        users Table columns:
            email: String, and can't be NULL.
            password: String, and can't be NULL.
            first_name: String, and can be NULL.
            last_name: String, and can be NULL.
        places relationship:
            Linked to the Place class.
        reviews relationship:
            Linked to the Review class.
    For File Storage:
        Attributes:
            email: String
            password: String
            first_name: String
            last_name: String
    '''
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user",
                              cascade="delete")
        reviews = relationship("Review", cascade="delete", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
