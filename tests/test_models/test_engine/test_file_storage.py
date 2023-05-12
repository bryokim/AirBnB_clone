#!/usr/bin/env python3
"""Test module for FileStorage class"""

import unittest
import uuid
import json
import os
from datetime import datetime

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

storage = FileStorage()


class TestFileStorageAllMethod(unittest.TestCase):
    """Class for testing the all method"""

    def test_return_value_is_dict(self):
        """Test that the all method retuns a dictionary"""
        self.assertIsInstance(storage.all(), dict)

    def test_values_in_dict_are_from_BaseModel(self):
        """Test that all values in __objects are either instances
        of BaseModel or inherit from it"""
        for obj in storage.all().values():
            self.assertIsInstance(obj, BaseModel)

    def test_calling_all_with_argument(self):
        """Test that calling all with an argument causes TypeError"""
        with self.assertRaises(TypeError):
            storage.all(12)


class TestFileStorageNewMethod(unittest.TestCase):
    """Class for testing the new method"""

    def setUp(self):
        """Setup variables used in tests"""
        self.kwargs = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
            }
        self.instance = BaseModel(**self.kwargs)

    def test_new_object_is_added_to_objects(self):
        """Test that a new object is added to __objects dictionary"""
        objects_before_updating = storage.all().copy()
        storage.new(self.instance)
        self.assertNotEqual(objects_before_updating, storage.all())

    def test_key_of_new_object(self):
        """Test that the key of the new object is of correct format"""
        expected = f'{self.instance.__class__.__name__}.{self.instance.id}'
        storage.new(self.instance)
        self.assertTrue(storage.all()[expected] is self.instance)

    def test_new_object_without_id(self):
        """Test that an attribute error occurs if object passed has no id"""
        del self.instance.id
        with self.assertRaises(AttributeError):
            storage.new(self.instance)

    def test_passing_int_object_argument(self):
        """Test that passing an integer raises attribute error"""
        with self.assertRaises(AttributeError):
            storage.new(112)

    def test_passing_float_object_argument(self):
        """Test that passing a float raises attribute error"""
        with self.assertRaises(AttributeError):
            storage.new(1.12)

    def test_passing_str_object_argument(self):
        """Test that passing a string raises attribute error"""
        with self.assertRaises(AttributeError):
            storage.new('one')

    def test_passing_dict_object_argument(self):
        """Test that passing a dict raises attribute error"""
        with self.assertRaises(AttributeError):
            storage.new({'name': 'Brian'})

    def test_passing_list_object_argument(self):
        """Test that passing a list raises attribute error"""
        with self.assertRaises(AttributeError):
            storage.new(['one'])

    def test_passing_tuple_object_argument(self):
        """Test that passing a tuple raises attribute error"""
        with self.assertRaises(AttributeError):
            storage.new(('one',))


class TestFileStorageSaveMethod(unittest.TestCase):
    """Class for testing the save method"""

    def test_save_method_writes_to_file(self):
        """Test that the save method updates the file when it's called"""
        storage.save()
        try:
            with open('file.json', 'r') as f:
                before_saving = json.load(f)
        except FileNotFoundError:
            before_saving = {}
        for i in range(5):
            BaseModel()
        storage.save()
        with open('file.json', 'r') as f:
            after_saving = json.load(f)
        self.assertTrue(len(before_saving) < len(after_saving))
        self.assertEqual(len(after_saving) - len(before_saving), 5)

    def test_passing_argument_to_save(self):
        """Test that passing an argument to save raises TypeError"""
        with self.assertRaises(TypeError):
            storage.save(1)


class TestFileStorageReloadMethod(unittest.TestCase):
    """Class for testing the reload method """

    def setUp(self):
        """Setup variables to use in tests"""

        BaseModel()
        storage.save()
        self.objects = storage.all()

    def tearDown(self):
        """Clean up after the tests"""

        for obj in self.objects.values():
            storage.new(obj)
        storage.save()

    def test_reload_from_unsvailable_file(self):
        """Test that reloading from a none existing file doesn't cause
        any errors"""
        os.remove('file.json')
        storage.reload()
