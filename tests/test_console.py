#!/usr/bin/python3
"""Module for testing the console"""

import uuid
import unittest
import sys
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


class TestConsoleCreate(unittest.TestCase):
    """Class for testing the create command"""

    def test_create_with_no_arguments(self):
        """Test that create prints '** class name missing **' if called without
        any arguments"""
        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create')
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    def test_create_BaseModel(self):
        """Test creating new BaseModel"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create BaseModel')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'BaseModel.{str(instance_id)}'])

    def test_create_User(self):
        """Test creating new User"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create User')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'User.{str(instance_id)}'])

    def test_create_Place(self):
        """Test creating new Place"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create Place')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'Place.{str(instance_id)}'])

    def test_create_City(self):
        """Test creating new City"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create City')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'City.{str(instance_id)}'])

    def test_create_Amenity(self):
        """Test creating new Amenity"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create Amenity')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'Amenity.{str(instance_id)}'])

    def test_create_Review(self):
        """Test creating new Review"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create Review')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'Review.{str(instance_id)}'])

    def test_create_State(self):
        """Test creating new State"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('create State')
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'State.{str(instance_id)}'])


class TestConsoleShow(unittest.TestCase):
    """Class for testing the show command"""

    def test_show_without_any_argument(self):
        """Test that show prints '** class name missing **' if it's called
        without any arguments"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd('show')
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    def test_show_with_correct_class_and_id(self):
        """Test that show prints string representation of available instance"""

        instance = BaseModel()
        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd(f'show BaseModel {instance.id}')
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, str(instance))

    def test_show_with_invalid_class_and_valid_id(self):
        """Test that show prints '** class doen't exist **' if the class name
        is not found to be valid"""

        instance = BaseModel()
        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd(f'show Class {instance.id}')
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class doesn't exist **")

    def test_show_with_valid_class_and_invalid_id(self):
        """Test that show prints '** no instance found **' if the class name
        is correct but id is wrong"""

        with patch('sys.stdout', StringIO()) as output:
            HBNBCommand().onecmd(f'show BaseModel {str(uuid.uuid4())}')
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** no instance found **")


if __name__ == '__main__':
    unittest.main()
