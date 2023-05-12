#!/usr/bin/env python3
"""Module for User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """User Class"""

    email = ''
    password = ''
    first_name = ''
    last_name = ''

    def __init__(self, *args, **kwargs):
        """Initialize a new User instance.

        Args:
            args (tuple): Tuple of attribute values. Not used.
            kwargs (dict): Dictionary of attribute/value pairs.
        """
        super().__init__(*args, **kwargs)
