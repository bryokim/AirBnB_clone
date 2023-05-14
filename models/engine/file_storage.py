#!/usr/bin/python3
"""Module with FileStorage class implementation"""

import json


class FileStorage(object):
    """FileStorage class implementation"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __object"""

        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id
        Args:
            obj (object): New object
        """

        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serealizes __objects to the JSON file"""

        objects_dict = {
            key: value.to_dict()
            for key, value in FileStorage.__objects.items()
            }
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objects_dict, f, indent=4)

    def reload(self):
        """Deserealizes the json file to __objects"""

        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.amenity import Amenity
        from models.city import City
        from models.review import Review
        from models.state import State

        classes = {
            'User': User,
            'BaseModel': BaseModel,
            'Place': Place,
            'Amenity': Amenity,
            'City': City,
            'State': State,
            'Review': Review,
        }

        try:
            with open(FileStorage.__file_path, "r") as f:
                loaded_dict = json.load(f)
            FileStorage.__objects = {
                key: eval(value['__class__'], classes)(**value)
                for key, value in loaded_dict.items()
                }
        except FileNotFoundError:
            pass
