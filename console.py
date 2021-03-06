#!/usr/bin/python3
'''
    Implementing the console for the HBnB project.
'''
import re
import cmd
import json
import shlex
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    '''
    Contains the entry point of the command interpreter.
    '''

    prompt = ("(hbnb) ")

    def do_quit(self, args):
        '''
        Quit command to exit the program.
        '''
        return True

    def do_EOF(self, args):
        '''
        Exits after receiving the EOF signal.
        '''
        return True

    def do_create(self, args):
        '''
        Create a new instance of a class passed in the command line.
        The first parameter MUST be a class object. More paramaters can
            be passed, but need to be passed as <key>="<value>" pairs.
        Prints out the id of the new object.
        Usage:
            create <class> <param2> ...
        Example 1:
            create State name="California"
        Example 2:
            create State
        '''
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            args = re.split("\s|=", args)
            new_instance = eval(args[0])()

            for idx in range(1, len(args), 2):
                key = args[idx]
                value = args[idx + 1]
                try:
                    new_instance.__getattribute__(key)
                except AttributeError:
                    continue
                if re.search("^\".*\"$", value) is not None:
                    value = value.replace("_", " ")
                    value = value.replace("\"", "")
                elif "." in value:
                    value = float(value)
                elif re.search("\d.*", value) is not None:
                    value = int(value)
                else:
                    continue
                setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")
            return

    def do_show(self, args):
        '''
        Print the string representation of an instance based on
            the class name and id passed on the command line.
        Usage:
            show <class> <param2>
        Example:
            show State 8f165686-c98d-46d9-87d9-d6059ade2d99
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        storage = models.storage
#        storage = FileStorage()
        storage.reload()
        obj_dict = storage.all()
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        key = args[0] + "." + args[1]
        try:
            value = obj_dict[key]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        '''
        Deletes an instance based on the class name and id passed on the
            command line.
        Usage:
            destroy <class> <param2>
        Example:
            destroy State 8f165686-c98d-46d9-87d9-d6059ade2d99
        '''
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        class_name = args[0]
        class_id = args[1]
        storage = models.storage
        storage.reload()
        obj_dict = storage.all()
        try:
            eval(class_name)
        except NameError:
            print("** class doesn't exist **")
            return
        key = class_name + "." + class_id
        try:
            del obj_dict[key]
        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        '''
        Prints all string representations of instances if no class is passed.
        Can pass a class to print all instances of that class.
        Usage:
            all (<class>)
        Example 1:
            all
        Example 2:
            all State
        '''
        obj_list = []
        storage = models.storage
        storage.reload()
        try:
            if len(args) != 0:
                eval(args)
            if len(args) == 0:
                objects = storage.all()
            else:
                objects = storage.all(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)

        print(obj_list)

    def do_update(self, args):
        '''
        Update an instance based on the class name, id, attribute name, and
            value of the attribute passed on the command line.
        Usage:
            update <class> <id> <attribute name> <value of attribute>
        Example:
            update State 8f165686-c98d-46d9-87d9-d6059ade2d99 name "Colorado"
        '''
        storage = models.storage
        storage.reload()
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        key = args[0] + "." + args[1]
        obj_dict = storage.all()
        try:
            obj_value = obj_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass
        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def emptyline(self):
        '''
        Prevents printing anything when an empty line is passed.
        '''
        pass

    def do_count(self, args):
        '''
        Prints the number of instances of the class passed on the command line
            that are currently in storage.
        Usage:
            count <class>
        Example:
            count State
        '''
        obj_list = []
        storage = models.storage
        storage.reload()
        objects = storage.all()
        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, val in objects.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    obj_list.append(val)
            else:
                obj_list.append(val)
        print(len(obj_list))

    def default(self, args):
        '''
        Catches all the function names that are not expicitly defined.
        '''
        functions = {"all": self.do_all, "update": self.do_update,
                     "show": self.do_show, "count": self.do_count,
                     "destroy": self.do_destroy, "update": self.do_update}
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = functions[args[1]]
            func(cmd_arg)
        except:
            print("*** Unknown syntax:", args[0])


if __name__ == "__main__":
    '''
    Entry point for the loop.
    '''
    HBNBCommand().cmdloop()
