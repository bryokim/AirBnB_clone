#!/usr/bin/env python3
"""Module containing Amenity class implementation."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class."""

    name = ''

    def __init__(self, *args, **kwargs):
        """Initialize a Amenity instance.

        Args:
            args (tuple): Tuple of attribute values. Not used.
            kwargs (dict): Dictionary of attribute/value pairs.
        """
        super().__init__(*args, **kwargs)
