#!/usr/bin/env python3
"""Modeule for testing the Place class"""

import unittest
import uuid
from datetime import datetime

from models.place import Place
from models.base_model import BaseModel
from models import storage


class TestPlaceInstanciatesNoArgs(unittest.TestCase):
    """Class testing instanciation of Place Class without arguments"""

    def setUp(self):
        """Setup instance to be used in testing"""
        self.instance = Place()

    def test_place_init_no_args(self):
        """Test the initialization of a Place instance without any
        arguments given."""
        self.assertIsInstance(self.instance, Place)

    def test_place_inherits_from_basemodel(self):
        """Test that the Place class inherits from the BaseModel class"""
        self.assertIsInstance(self.instance, BaseModel)

    def test_id_is_str(self):
        """Test that the id attr is a public instance attr and is a str"""
        self.assertIsInstance(self.instance.id, str)

    def test_created_at_is_datetime(self):
        """Test that the created_at attr is a public instance attr and is a
        datetime"""
        self.assertIsInstance(self.instance.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that the updated_at attr is a public instance attr and is a
        datetime"""
        self.assertIsInstance(self.instance.updated_at, datetime)

    def test_created_at_and_updated_at_are_different(self):
        """Test that created_at and updated_at attrs are different"""
        self.assertNotEqual(self.instance.created_at, self.instance.updated_at)

    def test_id_is_uuid4(self):
        """Test that id is a valid uuid4"""
        instance_id = uuid.UUID(self.instance.id)
        self.assertEqual(instance_id.version, 4)

    def test_save_after_creating_new_object(self):
        """Test that the newly created object is saved"""
        objects_before = storage.all().copy()
        Place()
        self.assertNotEqual(objects_before, storage.all())


class TestPlaceIntanciateWithAgs(unittest.TestCase):
    """Class for testing instanciation of a Place with args"""

    def test_args_instantiates(self):
        """Test that a completely new instance is created when *args is given
        despite of the values in args."""
        args = (str(uuid.uuid4()), datetime.now(), datetime.now())
        instance = Place(*args)
        self.assertNotEqual(instance.id, args[0])
        self.assertNotEqual(instance.created_at, args[1])
        self.assertNotEqual(instance.updated_at, args[2])

    def test_instantiation_with_single_integer(self):
        """Test instanciation with a single value"""
        instance = Place(1)
        self.assertIsInstance(instance.id, str)
        self.assertIsInstance(instance.created_at, datetime)
        self.assertIsInstance(instance.updated_at, datetime)


class TestPlaceWithKwargs(unittest.TestCase):
    """Class for testing initialization of Place with kwargs"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = Place()
        self.kwargs = self.instance.to_dict()
        self.new = Place(**self.kwargs)

    def test_kwargs_instanciates(self):
        """Test that an instance is loaded when kwargs is given. No new
        instance is created"""
        self.assertEqual(self.new.__dict__, self.instance.__dict__)

    def test_class_key_is_not_set(self):
        """Test that the __class__ key added is not set when using kwargs"""
        self.assertTrue(self.kwargs['__class__'])
        with self.assertRaises(KeyError):
            self.new.__dict__['__class__']

    def test_created_at_is_datetime_object(self):
        """Test that created_at is a datetime object derived from the
        iso format string in kwargs."""
        self.assertEqual(type(self.new.created_at), datetime)
        self.assertIsInstance(self.new.created_at, datetime)

    def test_updated_at_is_datetime_object(self):
        """Test that updated_at is a dateime object derived from the
        iso format string in kwargs"""
        self.assertEqual(type(self.new.updated_at), datetime)
        self.assertIsInstance(self.new.updated_at, datetime)

    def test_created_at_not_iso_format(self):
        """Test that an error occurs when the created_at value is not
        an iso formatted string"""
        self.kwargs['created_at'] = datetime.now()
        with self.assertRaises(TypeError):
            Place(**self.kwargs)
        self.kwargs['created_at'] = '12:00:00'
        with self.assertRaises(ValueError):
            Place(**self.kwargs)

    def test_updated_at_not_iso_format(self):
        """Test that an error occurs when the updated_at value is not
        an iso formatted string"""
        self.kwargs['updated_at'] = datetime.now()
        with self.assertRaises(TypeError):
            Place(**self.kwargs)
        self.kwargs['updated_at'] = '12:00:00'
        with self.assertRaises(ValueError):
            Place(**self.kwargs)

    def test_id_not_uuid4(self):
        """Test that no error occurs when id in kwargs is not of type
        uuid4."""
        self.kwargs['id'] = '123'
        self.assertTrue(Place(**self.kwargs))
        self.kwargs['id'] = 123
        self.assertTrue(Place(**self.kwargs))

    def test_empty_kwargs(self):
        """Test that an empty kwargs causes new instance to be creates"""
        self.kwargs = {}
        objects_before = storage.all().copy()
        Place(**self.kwargs)
        self.assertTrue(objects_before != storage.all())

    def test_kwargs_missing_one_attribute(self):
        """Test that a kwargs missing an attribute doesn't cause new object
        creation"""
        del self.kwargs['id']
        new_instance = Place(**self.kwargs)
        with self.assertRaises(AttributeError):
            new_instance.id

    def test_new_instance_is_not_original(self):
        """Test that an instance loaded from anothers dictionary is not
        identical to the original"""
        self.assertFalse(self.instance is self.new)


class TestPlaceWithArgsAndKwargs(unittest.TestCase):
    """Class for testing instantiation with both args and kwargs"""

    def setUp(self):
        """Setup instance to be used in testing"""
        self.instance = Place()
        self.kwargs = self.instance.to_dict()
        self.args = (uuid.uuid4(), datetime.now(), datetime.now())

    def test_args_and_kwargs_instanciates(self):
        """Test that kwargs is used instead of args in instanciation."""
        new_instance = Place(*self.args, **self.kwargs)
        self.assertEqual(self.instance.__dict__, new_instance.__dict__)

    def test_no_new_object_is_created(self):
        """Test that a new object is not added to the objects in storage"""
        before_loading = storage.all().copy()
        Place(*self.args, **self.kwargs)
        self.assertTrue(before_loading == storage.all())


class TestPlaceStrMethod(unittest.TestCase):
    """Class for testing the __str__ method """

    def test_str_representation(self):
        """Test that the str representation of the Place instance is
        formatted correctly"""
        instance = Place()
        expected = "[{}] ({}) {}".format(
            instance.__class__.__name__, instance.id,
            instance.__dict__)
        self.assertEqual(expected, str(instance))


class TestPlaceToDictMethod(unittest.TestCase):
    """Class for testing the to_dict method"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = Place()

    def test_value_of_class_key(self):
        """Test that the __class__ key has the correct class name ie. Place"""
        self.assertEqual(self.instance.to_dict()['__class__'], 'Place')
