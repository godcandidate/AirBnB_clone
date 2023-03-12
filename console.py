#!/usr/bin/python3
"""
This module contains `HBNBCommand` class
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import re

class HBNBCommand(cmd.Cmd):
    """
    This contains entry point of the command interpreter
    Attributes:
        prompt (str): the console prompt text
        __classes (list): list of available classes
    """

    prompt = '(hbnb) '
    __classes = [
            'BaseModel',
            'User',
            'State',
            'City',
            'Amenity',
            'Place',
            'Review'
            ]

    def do_quit(self, arg):
        """Exits the comand line interface
        """
        return True

    def do_EOF(self, arg):
        """
        Exits the comand line interface
        Usage: (press Ctrl-D ord Ctrl-Z to exit)
        """
        return True

    def emptyline(self):
        """
        Does nothing
        Usage: (Press Enter)
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        Usage:
            create <classname>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{args[0]}()")
            print(new_instance.id)
            storage.save()

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        usage:
            show <classname> <class.id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            """
            dict1: storage.all()
            key: f"{args[0]}.{args[1]}"
            print(dict1[key])
            """
            print(storage.all()[f"{args[0]}.{args[1]}"])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id (save the change into the JSON file
        usage:
            delete <classname> <class.id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[f"{args[0]}.{args[1]}"]
            storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        usage:
            all or all <classname>
        """
        args = arg.split()
        if len(args) == 0:
            print([str(value) for value in storage.all().values()])
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        else:
            """
            dict1: objs
            string: args[0]
            list1 = []
            for k,v in dict1:
                if k.startswith(string):
                    list1.append[value]
            print(list1)
            """
            objs = storage.all().items()
            print([str(v) for k, v in objs if k.startswith(args[0])])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        usage:
            update <classname> <classid> <new/old attribute> <value>
        """
        args = arg.split()

        if len(arg) == 0:
            print("** class name missing **")
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("instance id missing")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            obj_class = args[0]
            obj_id = args[1]
            obj_key = obj_class + "." + obj_id
            obj = storage.all()[obj_key]

            attr_name = args[2]
            attr_value = args[3]

            """
            checks if attr_value contains "
            exp: attr_value = "Betty"
            converts to attr_value = Betty
            """
            if attr_value[0] == '"':
                attr_value = attr_value[1:-1]

            """
            if - checks the object has the specified attribute
                if - checks the attribute has type str/int/float
            else - creates a new attribute and assign a value
            """
            if hasattr(obj, attr_name):
                type_ = type(getattr(obj, attr_name))
                types = [str, int, float]

                if type_ in types:
                    attr_value = type_(attr_value)
                    setattr(obj, attr_name, attr_value)

            else:
                setattr(obj, attr_name, attr_value)
            storage.save()

    def default(self, arg):
        """
        <class name>.[special commands]
        special commands:
            all() - print all objects of the class
            count() - count all objects of the class
            show(<id>) - show object with class id
            destroy(<id>) - delete object with class is
            update(<id>, <attribute name>, <attribute value>) - update
            update(<id>, <dictionary representation>) - update

        """
        args = arg.split('.')

        if args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif args[1] == "all()":
            self.do_all(args[0])
        elif args[1] == "count()":
            objs = storage.all().items()
            len_ = len([k for k, v in objs if k.startswith(args[0])])
            print(len_)
        elif args[1].startswith("show"):
            id_ = args[1].split('"')[1]
            self.do_show(f"{args[0]} {id_}")
        elif args[1].startswith("destroy"):
            id_ = args[1].split('"')[1]
            self.do_destroy(f"{args[0]} {id_}")
        elif args[1].startswith("update"):
            params = args[1].split('"')
            id_ = params[1]
            pattern = r'\{[^\}]*\}'
            dict_ = re.search(pattern, args[1])

            if dict_:
                dict_ = eval(dict_.group())
                for k, v in dict_.items():
                    self.do_update(f"{args[0]} {id_} {k} {v}")
            else:
                attr_name = params[3]
                attr_value = params[5]

                self.do_update(f"{args[0]} {id_} {attr_name} {attr_value}")
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
