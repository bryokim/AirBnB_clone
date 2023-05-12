#!/usr/bin/env python3
"""Module containing City class implementation."""
from models.base_model import BaseModel


class City(BaseModel):
    """City class."""

    name = ''
    state_id = ''

    def __init__(self, *args, **kwargs):
        """Initialize a City instance.

        Args:
            args (tuple): Tuple of attribute values. Not used.
            kwargs (dict): Dictionary of attribute/value pairs.
        """
        super().__init__(*args, **kwargs)
