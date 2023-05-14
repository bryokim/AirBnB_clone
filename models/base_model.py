#!/usr/bin/python3
"""Module containing the BaseModel class implementation"""

import uuid
from datetime import datetime

from models import storage


class BaseModel(object):
    """BaseModel Class"""

    def __init__(self, *args, **kwargs):
        """Initialize a BaseModel instance

        Args:
            args (tuple): Tuple of arguments.
            kwargs (dict): Dictionary of attr/value pairs

        """

        if kwargs:
            timestamps = ['created_at', 'updated_at']
            for attr, value in kwargs.items():
                if attr != '__class__':
                    if attr in timestamps:
                        value = datetime.fromisoformat(value)
                    setattr(self, attr, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return string representation of a BaseModel instance

            Returns:
                str: String representation of BaseModel instance
        """

        return "[{0}] ({1}) {2}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at with
        the current datetime"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all __dict__ key/values of
        the instance. A __class__ key is added with name of object.

        Returns:
            dict: Dictionary representation of the instance.
        """

        instance_dict = {
            key: (value.isoformat() if type(value) is datetime else value)
            for key, value in self.__dict__.items()
            }
        instance_dict['__class__'] = self.__class__.__name__

        return instance_dict
