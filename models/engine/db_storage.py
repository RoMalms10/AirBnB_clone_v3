#!/usr/bin/python3
'''
    Implementation of the DBStorage class.
'''
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session, exc
import os


class DBStorage():
    '''
    DBStorage Class.
    A type of storage method that uses MySQL to store data.
    When the environment variable HBNB_TYPE_STORAGE is equal to db, this
        storage method will be used.
     Methods:
        __init__
        all
        new
        save
        delete
        reload
        close
        get
        count
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
        Scans the environment variables to connect to a database.
        Then, creates a connection to the engine.
        '''
        username = os.getenv('HBNB_MYSQL_USER', default=None)
        password = os.getenv('HBNB_MYSQL_PWD', default=None)
        localhost = os.getenv('HBNB_MYSQL_HOST', default=None)
        db_name = os.getenv('HBNB_MYSQL_DB', default=None)
        connection = 'mysql+mysqldb://{}:{}@localhost/{}'
        self.__engine = create_engine(connection.format(
            username, password, db_name), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        Queries current database session.
        This query can take in a class or not. If no class is passed, returns
            all objects in the database. If a class is passed, returns
            all objects of that type.
        Arguments:
            cls: Class passed, defaults to None.
        Returns:
            Dictionary representation of the query in the form of:
                key: str(object).id
                value: the actual object with that id
        '''
        result = []
        new_dict = {}
        if cls is not None:
            result = self.__session.query(eval(cls)).all()
            for item in result:
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item
        else:
            classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
            for class_name in classes:
                try:
                    result = (self.__session.query(eval(class_name)).all())
                    for item in result:
                        key = item.__class__.__name__ + '.' + item.id
                        new_dict[key] = item
                except Exception:
                    continue
        return new_dict

    def new(self, obj):
        '''
        Adds the object to the current database session.
        Arguments:
            obj: object passed
        '''
        self.__session.add(obj)

    def save(self):
        '''
        Saves all changes of the current session by committing the changes
            to the database.
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
        Deletes the object from storage by deleting it in the database and
            saving.
        Arguments:
            obj: object passed, defaults to None
        '''
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        '''
        Creates all tables in the database.
        '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        '''
        Closes the current session with the database.
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
        Method that retrieves an object based off the class (cls) passed
        and the id (id) passed
        Arguments:
            cls: string representing the class name
            id: string representing the object ID
        Attributes:
            cls_dict: the dictionary received from the all method when
                passing a class.
        Returns:
            the object if found, or nothing
        '''
        cls_dict = self.all(cls)

        if len(cls_dict) == 0:
            return None
        key = cls + '.' + id
        if key in cls_dict:
            return cls_dict[key]
        else:
            return None

    def count(self, cls=None):
        '''
        Method that counts how many objects of the type cls being passed.
        Arguments:
            cls: string representing the class name (optional)
        Attributes:
            all_dict: the dictionary received from the all method when no
                class is passed.
            cls_dict: the dictionary received from the all method when
                pasing a class.
        Returns:
            The count of objects
        '''
        cls_dict = {}
        all_dict = {}

        if cls is None:
            all_dict = self.all()
            return len(all_dict)
        else:
            cls_dict = self.all(cls)
            return len(cls_dict) 
