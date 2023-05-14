#!/usr/bin/python3
"""Module containing command interpreter"""
import cmd
import json

from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models import storage


class HBNBCommand(cmd.Cmd):
    """HBNBCommand Class"""

    prompt = '(hbnb) '

    objects = storage.all()
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Amenity': Amenity,
        'Place': Place,
        'City': City,
        'Review': Review,
        'State': State,
    }

    @staticmethod
    def __check_class_and_id(cmd, line):
        """Validate class and id for given command.

        Args:
            cmd (str): Command to be executed.
            line (str): Arguments to the command.

        Returns:
            str: Key of the current object in the objects dictionary.
                If arguments were invalid an empty string is returned.
        """
        err_msg = ""
        if not line:
            err_msg = "** class name missing **"
        else:
            args = line.split()

            if args[0] not in HBNBCommand.classes:
                err_msg = "** class doesn't exist **"
            if cmd != 'create' and not err_msg:
                if len(args) == 1:
                    err_msg = "** instance id missing **"
                elif f'{args[0]}.{args[1]}' not in HBNBCommand.objects:
                    err_msg = "** no instance found **"

        key = ''
        if err_msg:
            print(err_msg)
        elif cmd == 'create':
            key = f'{args[0]}'
        else:
            key = f'{args[0]}.{args[1]}'

        return key

    def do_create(self, line):
        """Creates a new instance of the given class.

        Args:
            line (str): Class to be created.
        """
        className = self.__check_class_and_id('create', line)

        if className:
            # new_obj = HBNBCommand.classes[className]()
            new_obj = eval(className)()
            new_obj.save()
            print(f"{new_obj.id}")

    def do_show(self, line):
        """Prints the string representation of an instance based on class
        name and id.

        Args:
            line (str): Class name and id.
        """
        key = self.__check_class_and_id('show', line)
        if key:
            print(HBNBCommand.objects[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.

        Args:
            line (str): Class name and id.
        """
        key = self.__check_class_and_id('destroy', line)
        if key:
            del HBNBCommand.objects[key]
            storage.save()

    def do_all(self, line):
        """Prints all string representations of all instances based on or
        not on the class name.

        Example:
        (hbnb) all -> Prints all string representations of all classes.
        (hbnb) all BaseModel -> Prints all string representations of BaseModel
            classes only.

        Args:
            line (str): Class name.
        """
        list_objs = []
        if not line:
            list_objs = [
                obj.__str__() for obj in HBNBCommand.objects.values()
                ]
        elif line.split()[0] in HBNBCommand.classes:
            list_objs = [
                obj.__str__() for obj in HBNBCommand.objects.values()
                if obj.__class__ .__name__ == line.split()[0]
                ]
        else:
            print("** class doesn't exist **")

        if list_objs:
            print(list_objs)

    @staticmethod
    def __check_update_args(line):
        """Validate arguments given to update command.

        Args:
            line (str): Space separated string of arguments.

        Returns:
            tuple: Tuple of key, attribute name and attribute value.
                An empty tuple is returned if argument is invalid.
        """

        key = HBNBCommand.__check_class_and_id('update', line)
        if key:
            args = line.split()
            err_msg = ''
            if len(args) == 2:
                err_msg = "** attribute name missing **"
            elif len(args) == 3:
                err_msg = "** value missing **"

            if err_msg:
                print(err_msg)
                return ()
        else:
            return ()

        attr_name = args[2]
        attr_value = args[3]
        if attr_value[0] in '"\'':
            i = 4
            while i < len(args):
                attr_value += f' {args[i]}'
                if args[i][-1] in '"\'':
                    break
                i += 1

        return (key, attr_name, attr_value.strip(' "\''))

    def do_update(self, line):
        """Updates an instance based on class name and id by adding or
        updating attribute.

        Attribute value is cast to the attribute type.

        Args:
            line (str): Class name, id, attribute name and attribute value.
        """

        args = self.__check_update_args(line)
        if args:
            key, attr_name, attr_value = args
            obj = HBNBCommand.objects[key]
            if attr_value.isdigit():
                attr_value = int(attr_value)
            elif attr_value.replace('.', '', 1).isdigit():
                attr_value = float(attr_value)
            setattr(obj, attr_name, attr_value)
            obj.save()

    def do_count(self, line):
        """Count the number of instaces of a given class

        Args:
            line (str): Class name
        """
        if line in HBNBCommand.classes:
            count = 0
            for obj in HBNBCommand.objects.values():
                if obj.__class__.__name__ == line:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    @staticmethod
    def parse_default_args(line):
        """Parse arguments from default commands.

        Args:
            line (str): String containing arguments and command.

        Returns:
            tuple: Tuple of the arguments parsed from the string given.
                The tuple consists of:
            (<class name>, <instance id>, <attribute name>, <attribute value>)
        """
        args = line.split('.', 1)
        # Get arguments within the braces
        brace_args = args[1].split('(')[1].strip(')').split(',')

        arguments_tuple = (args[0],)  # class name
        if len(brace_args) >= 1:
            arguments_tuple += (brace_args[0].strip(' \'"'),)  # instance id
        if len(brace_args) >= 2:
            arguments_tuple += (brace_args[1].strip(' \'"'),)  # attribute name
        if len(brace_args) >= 3:
            arguments_tuple += (brace_args[2].strip(),)  # attribute value

        return arguments_tuple

    def __update_from_default(self, line):
        """Handles updating from the default syntax.

        Syntax:
            <class name>.update(<id>, <attribute name>, <attribute value>)
            <class name>.update(<id>, <dictionary representation>)

        Args:
            line (str): Command as passed in console.

        Raises:
            TypeError: If the attributes and values are not in dictionary
                representation.
        """
        try:
            # Try loading the dictionary to a variable.
            # Raises IndexError or json.decoder.JSONDecodeError.
            attrs = json.loads(
                line.split('.', 1)[1].split('(', 1)[1].strip(')').
                split(',', 1)[1].replace("'", '"')
            )
            if type(attrs) is not dict:
                raise TypeError

            # Get class name and id from first two elements of arguments tuple
            className, instance_id = self.parse_default_args(line)[:2]

            # Check if object exists before looping through attributes.
            # Print only one error message instead of numerous.
            if f'{className}.{instance_id}' in HBNBCommand.objects:
                for attr_name, attr_value in attrs.items():
                    self.do_update(
                        f'{className} {instance_id} {attr_name} "{attr_value}"'
                    )
            else:
                print("** no instance found")

        except IndexError:
            args = self.parse_default_args(line)
            self.do_update(' '.join(args))
        except TypeError:
            args = self.parse_default_args(line)
            self.do_update(' '.join(args))
        except json.decoder.JSONDecodeError:
            args = self.parse_default_args(line)
            self.do_update(' '.join(args))

    def default(self, line):
        """Run default commands.
        Format:
            <class name>.all()
            <class name>.count()
            <class name>.show(<id>)
            <class name>.destroy(<id>)
            <class name>.update(<id>, <attribute name>, <attribute value>)
            <class name>.update(<id>, <dictionary representation>)

        Args:
            line (str): Command to be executed. Can be any of the above
            formats.
        """
        try:
            command = line.split('.', 1)[1].split('(')[0]
            func = getattr(self, f'do_{command}')
            if command == 'update':
                self.__update_from_default(line)
            else:
                args = self.parse_default_args(line)
                func(' '.join(args).strip())
        except IndexError:
            print(f'*** Unknown syntax: {line}')
        except AttributeError:
            print(f'*** Unknown syntax: {line}')

    def do_EOF(self, line):
        """Exit program when EOF is encountered"""
        return True

    def do_quit(self, line):
        """Exit the program
        Args:
            line (str): Argument to command
        """
        return True

    def emptyline(self):
        """Do nothing if empty line"""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
