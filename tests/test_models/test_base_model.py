#!/usr/bin/env python3
"""Test module for BaseModel class"""
import unittest
import uuid
from datetime import datetime

from models.base_model import BaseModel
from models import storage


class TestBaseModelNoArg(unittest.TestCase):
    """Class for testing initialization of BaseModel with no args"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = BaseModel()

    def test_no_args_instantiates(self):
        """Test that an instance is created when no arguments are passed"""
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

    def test_created_at_and_updated_at_are_datetime_objects(self):
        """Test that created_at and updated_at attrs are datetime objects"""
        self.assertEqual(type(self.instance.created_at), datetime)
        self.assertEqual(type(self.instance.updated_at), datetime)

    def test_id_is_uuid4(self):
        """Test that id is a valid uuid4"""
        instance_id = uuid.UUID(self.instance.id)
        self.assertEqual(instance_id.version, 4)

    def test_str_representation(self):
        """Test that the str representation of the BaseModel instance is
        formatted correctly"""
        expected = "[{}] ({}) {}".format(
            self.instance.__class__.__name__, self.instance.id,
            self.instance.__dict__)
        self.assertEqual(expected, str(self.instance))

    def test_save_after_creating_new_object(self):
        """Test that the newly created object is saved"""
        objects_before = storage.all().copy()
        BaseModel()
        self.assertNotEqual(objects_before, storage.all())


class TestBaseModelWithArgs(unittest.TestCase):
    """Class for testing initialization of BaseModel with args"""

    def test_args_instantiates(self):
        """Test that a completely new instance is created when *args is given
        despite of the values in args."""
        args = (str(uuid.uuid4()), datetime.now(), datetime.now())
        instance = BaseModel(*args)
        self.assertNotEqual(instance.id, args[0])
        self.assertNotEqual(instance.created_at, args[1])
        self.assertNotEqual(instance.updated_at, args[2])

    def test_instantiation_with_single_integer(self):
        """Test instanciation with a single value"""
        instance = BaseModel(1)
        self.assertIsInstance(instance.id, str)
        self.assertIsInstance(instance.created_at, datetime)
        self.assertIsInstance(instance.updated_at, datetime)


class TestBaseModelWithKwargs(unittest.TestCase):
    """Class for testing initialization of BaseModel with kwargs"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = BaseModel()
        self.kwargs = self.instance.to_dict()
        self.new = BaseModel(**self.kwargs)

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
            BaseModel(**self.kwargs)
        self.kwargs['created_at'] = '12:00:00'
        with self.assertRaises(ValueError):
            BaseModel(**self.kwargs)

    def test_updated_at_not_iso_format(self):
        """Test that an error occurs when the updated_at value is not
        an iso formatted string"""
        self.kwargs['updated_at'] = datetime.now()
        with self.assertRaises(TypeError):
            BaseModel(**self.kwargs)
        self.kwargs['updated_at'] = '12:00:00'
        with self.assertRaises(ValueError):
            BaseModel(**self.kwargs)

    def test_id_not_uuid4(self):
        """Test that no error occurs when id in kwargs is not of type
        uuid4."""
        self.kwargs['id'] = '123'
        self.assertTrue(BaseModel(**self.kwargs))
        self.kwargs['id'] = 123
        self.assertTrue(BaseModel(**self.kwargs))

    def test_empty_kwargs(self):
        """Test that an empty kwargs causes new instance to be creates"""
        self.kwargs = {}
        objects_before = storage.all().copy()
        BaseModel(**self.kwargs)
        self.assertTrue(objects_before != storage.all())

    def test_kwargs_missing_one_attribute(self):
        """Test that a kwargs missing an attribute doesn't cause new object
        creation"""
        del self.kwargs['id']
        new_instance = BaseModel(**self.kwargs)
        with self.assertRaises(AttributeError):
            new_instance.id

    def test_new_instance_is_not_original(self):
        """Test that an instance loaded from anothers dictionary is not
        identical to the original"""
        self.assertFalse(self.instance is self.new)


class TestBaseModelWithArgsAndKwargs(unittest.TestCase):
    """Class for testing instantiation with both args and kwargs"""

    def setUp(self) -> None:
        self.instance = BaseModel()
        self.kwargs = self.instance.to_dict()
        self.args = (uuid.uuid4(), datetime.now(), datetime.now())

    def test_args_and_kwargs_instanciates(self):
        """Test that kwargs is used instead of args in instanciation."""
        new_instance = BaseModel(*self.args, **self.kwargs)
        self.assertEqual(self.instance.__dict__, new_instance.__dict__)

    def test_no_new_object_is_created(self):
        """Test that a new object is not added to the objects in storage"""
        before_loading = storage.all().copy()
        BaseModel(*self.args, **self.kwargs)
        self.assertTrue(before_loading == storage.all())


class TestBaseModelSaveMethod(unittest.TestCase):
    """Class for testing save method of BaseModel"""

    def setUp(self) -> None:
        """Setup variables for testing"""
        self.instance = BaseModel()

    def test_save_method_updates_updated_at(self):
        """Test that the save method updates the updated_at attribute"""
        first_updated_at = self.instance.updated_at
        self.instance.save()
        self.assertNotEqual(first_updated_at, self.instance.updated_at)

    def test_save_method_calls_save_on_storage(self):
        """Test that the save method calls save method on storage so as
        to write the new updated object to the file.json"""
        key = f'BaseModel.{self.instance.id}'
        first_updated_at = storage.all()[key]
        self.instance.save()
        storage.reload()
        self.assertNotEqual(first_updated_at, storage.all()[key])

    def test_save_method_does_not_affect_other_attributes(self):
        """Test that the save method does not affect created_at and id"""
        created_at, id = self.instance.created_at, self.instance.id
        self.instance.save()
        self.assertEqual(created_at, self.instance.created_at)
        self.assertEqual(id, self.instance.id)

    def test_save_method_with_argument(self):
        """Test that the save method raises an error when called with an
        argument"""
        with self.assertRaises(TypeError):
            self.instance.save(12)


class TestBaseModelToDictMethod(unittest.TestCase):
    """Class for testing the to_dict method"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = BaseModel()

    def test_to_dict_return_value_type_is_dctionary(self):
        """Test that the to_dict method returns a dictionary"""
        self.assertIsInstance(self.instance.to_dict(), dict)

    def test_to_dict_return_value_has_class_key(self):
        """Test that the to_dict return value has the __class__ key"""
        self.assertTrue(self.instance.to_dict()['__class__'])

    def test_created_at_iso_format_in_returned_dictionary(self):
        """Test that the created_at value is in iso format"""
        self.assertIsInstance(self.instance.to_dict()['created_at'], str)

    def test_updated_at_iso_format_in_returned_dictionary(self):
        """Test that the updated_at value is in iso format"""
        self.assertIsInstance(self.instance.to_dict()['updated_at'], str)

    def test_all_values_in_dict_are_in_returned_dictionary(self):
        """Test that the returned dictionary contains all values in the
        __dict__ of the instance"""
        instance_dict = self.instance.to_dict()
        for key in self.instance.__dict__.keys():
            self.assertTrue(key in instance_dict)

    def test_to_dict_with_arguments(self):
        """Test that to_dict raises an error when called with an argument"""
        with self.assertRaises(TypeError):
            self.instance.to_dict(12)
