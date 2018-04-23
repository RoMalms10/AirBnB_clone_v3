#!/usr/bin/python3
'''
    Define class FileStorage
'''
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return the dictionary
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
            Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        self.__objects[key] = value_dict

    def save(self):
        '''
            Serializes __objects attribute to JSON file.
        '''
        objects_dict = {}
        for key, val in self.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(self.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
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
        Deletes an object from __objects if it is inside of __objects
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
        Method calls reload method to deserialize JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        '''
        Method that retrieves an object based off the class (cls) passed
        and the id (id) passed
        Attributes:
            cls: string representing the class name
            id: string representing the object ID
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
        Attributes:
            cls: string representing the class name (optional)
        '''
        cls_dict = {}
        all_dict = {}

        if cls is None:
            all_dict = self.all()
            return len(all_dict)
        else:
            cls_dict = self.all(cls)
            return len(cls_dict)
