#!/usr/bin/env python3
"""Module containing Place class implementation."""
from models.base_model import BaseModel


class Place(BaseModel):
    """Place class."""

    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initialize a Place instance.

        Args:
            args (tuple): Tuple of attribute values. Not used.
            kwargs (dict): Dictionary of attribute/value pairs.
        """
        super().__init__(*args, **kwargs)
