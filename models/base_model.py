#!/usr/bin/python3
'''
    Implementation of the BaseModel class.
'''
import os
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    '''
    BaseModel Class.
    Base class for other classes to inherit from.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, the
        database method of storage will be used. No table is created, but
        columns used in other classes are created.
    For Database Storage:
        Table columns:
            id: String, can't be NULL, and is a primary key.
            created_at: DateTime, and can't be NULL.
            updated_at: DateTime, and can't be NULL.
    For File Storage:
        Attributes:
            id: String of UUID
            created_at: DateTime
            updated_at: DateTime
        Methods:
            __init__
            __str__
            __repr__
            save
            to_dict
            delete
    '''

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)

    def __init__(self, *args, **kwargs):
        '''
        Initialize public instance attributes.
        '''
        if (len(kwargs) == 0):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            try:
                time_format = "%Y-%m-%dT%H:%M:%S.%f"
                kwargs["created_at"] = datetime.strptime(kwargs["created_at"],
                                                         time_format)
                kwargs["updated_at"] = datetime.strptime(kwargs["updated_at"],
                                                         time_format)
            except KeyError:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
            for key, val in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, val)

    def __str__(self):
        '''
        Return string representation of self object.
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __repr__(self):
        '''
        Return string representation of self object.
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        '''
        Saves the current object to storage.
        updated_at also gets a new time based on when the save takes place.
        '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        '''
        Return dictionary representation of self object to be used when
            converting to JSON format.
        '''
        cp_dct = dict(self.__dict__)
        try:
            del cp_dct['_sa_instance_state']
        except KeyError:
            pass
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")

        return (cp_dct)

    def delete(self):
        '''
        Deletes the current self object from storage
            by calling the method delete in storage object.
        '''
        models.storage.delete(self)
