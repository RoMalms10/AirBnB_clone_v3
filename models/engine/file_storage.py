#!/usr/bin/python3
'''
    Implementation of the FileStorage class.
'''
import json
import models


class FileStorage:
    '''
    FileStorage Class.
    A type of storage method that uses JSON and files to store data.
    When the environment variable HBNB_TYPE_STORAGE is not equal to db, this
        storage method will be used.
     Methods:
        all
        new
        save
        delete
        reload
        close
        get
        count
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
        Loads all objects in storage and returns a dictionary.
        This method can take in a class or not. If no class is passed, returns
            all objects in the database. If a class is passed, returns
            all objects of that type.
        Arguments:
            cls: Class passed, defaults to None.
        Returns:
            Dictionary representation of the query in the form of:
                key: str(object).id
                value: the actual object with that id
        '''
        if cls is None:
            return self.__objects
        else:
            my_dict = {}
            for k, v in self.__objects.items():
                name = k.split('.')
                if name[0] in str(cls):
                    my_dict[k] = v
            return my_dict

    def new(self, obj):
        '''
        Adds the object to the current storage session by adding a key and
            value to the self.__objects dictionary.
        Arguments:
            obj: object passed
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        self.__objects[key] = value_dict

    def save(self):
        '''
        Saves all changes of the current session by committing the changes
            to the current storage session by serializes all the values in
            self.__objects to the JSON file.
        '''
        objects_dict = {}
        for key, val in self.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(self.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
        Deserializes the JSON file to self.__objects by populating key, value
            pairs and instanciating the objects in the values.
        '''
        try:
            with open(self.__file_path, encoding="UTF8") as fd:
                self.__objects = json.load(fd)
            for key, val in self.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                self.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Deletes the object from storage by deleting it in self.__objects and
            saving the dictionary back into the JSON file.
        '''
        copy_storage = dict(self.__objects)
        desired_key = obj
        for key, val in copy_storage.items():
            if val == desired_key:
                del(obj)
                del self.__objects[key]
                self.save()

    def close(self):
        '''
        Method calls reload method to deserialize JSON file to objects.
        '''
        self.reload()

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
