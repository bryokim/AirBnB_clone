#!/usr/bin/env python3

from . import file_storage


def import_all_classes():
    """Import all classes in models package.

    Returns:
        dict: Dictionary of class name/class pairs.
    """
    from models.base_model import BaseModel
    from models.user import User
    from models.place import Place
    from models.amenity import Amenity
    from models.city import City
    from models.review import Review
    from models.state import State

    return {
        'User': User,
        'BaseModel': BaseModel,
        'Place': Place,
        'Amenity': Amenity,
        'City': City,
        'State': State,
        'Review': Review,
    }
