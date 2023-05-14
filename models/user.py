#!/usr/bin/python3
"""Module for User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """User Class"""

    email = ''
    password = ''
    first_name = ''
    last_name = ''
