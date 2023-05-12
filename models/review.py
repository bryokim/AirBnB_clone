#!/usr/bin/env python3
"""Module containing Review class implementation."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class."""

    place_id = ''
    user_id = ''
    text = ''

    def __init__(self, *args, **kwargs):
        """Initialize a Review instance.

        Args:
            args (tuple): Tuple of attribute values. Not used.
            kwargs (dict): Dictionary of attribute/value pairs.
        """
        super().__init__(*args, **kwargs)
