#!/usr/bin/env python3
"""Module for testing the console"""

import uuid
import unittest
import sys
from io import StringIO

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


class TestConsoleCreate(unittest.TestCase):
    """Class for testing the create command"""

    def setUp(self):
        """Setup stdout"""
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        """Restore stdout"""
        sys.stdout = sys.__stdout__

    def test_create_with_no_arguments(self):
        """Test that create prints '** class name missing **' if called without
        any arguments"""
        HBNBCommand().onecmd('create')
        printed_str = self.output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    def test_create_BaseModel(self):
        """Test creating new BaseModel"""

        HBNBCommand().onecmd('create BaseModel')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'BaseModel.{str(instance_id)}'])

    def test_create_User(self):
        """Test creating new User"""

        HBNBCommand().onecmd('create User')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'User.{str(instance_id)}'])

    def test_create_Place(self):
        """Test creating new Place"""

        HBNBCommand().onecmd('create Place')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'Place.{str(instance_id)}'])

    def test_create_City(self):
        """Test creating new City"""

        HBNBCommand().onecmd('create City')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'City.{str(instance_id)}'])

    def test_create_Amenity(self):
        """Test creating new Amenity"""

        HBNBCommand().onecmd('create Amenity')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'Amenity.{str(instance_id)}'])

    def test_create_Review(self):
        """Test creating new Review"""

        HBNBCommand().onecmd('create Review')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'Review.{str(instance_id)}'])

    def test_create_State(self):
        """Test creating new State"""

        HBNBCommand().onecmd('create State')
        instance_id = uuid.UUID(self.output.getvalue().replace('\n', ''))
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f'State.{str(instance_id)}'])


class TestConsoleShow(unittest.TestCase):
    """Class for testing the show command"""

    def setUp(self):
        """Setup stdout"""
        self.instance = BaseModel()
        self.instance_id = self.instance.id
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        """Restore stdout"""
        sys.stdout = sys.__stdout__

    def test_show_without_any_argument(self):
        """Test that show prints '** class name missing **' if it's called
        without any arguments"""
        HBNBCommand().onecmd('show')
        printed_str = self.output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    def test_show_with_correct_class_and_id(self):
        """Test that show prints string representation of available instance"""
        HBNBCommand().onecmd(f'show BaseModel {self.instance_id}')
        printed_str = self.output.getvalue().replace('\n', '')
        self.assertEqual(printed_str, str(self.instance))

    def test_show_with_invalid_class_and_valid_id(self):
        """Test that show prints '** class doen't exist **' if the class name
        is not found to be valid"""
        HBNBCommand().onecmd(f'show Class {self.instance_id}')
        printed_str = self.output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class doesn't exist **")

    def test_show_with_valid_class_and_invalid_id(self):
        """Test that show prints '** no instance found **' if the class name
        is correct but id is wrong"""
        HBNBCommand().onecmd('show BaseModel 1234')
        printed_str = self.output.getvalue()[:-1]
        self.assertEqual(printed_str, "** no instance found **")
