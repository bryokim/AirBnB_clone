#!/usr/bin/env python3
"""Modeule for testing the User class"""

import unittest
import uuid
from datetime import datetime

from models.user import User
from models.base_model import BaseModel
from models import storage


class TestUserInstanciatesNoArgs(unittest.TestCase):
    """Class testing instanciation of User Class without arguments"""

    def setUp(self):
        """Setup instance to be used in testing"""
        self.instance = User()

    def test_user_init_no_args(self):
        """Test the initialization of a User instance without any
        arguments given."""
        self.assertIsInstance(self.instance, User)

    def test_user_inherits_from_basemodel(self):
        """Test that the User class inherits from the BaseModel class"""
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
        User()
        self.assertNotEqual(objects_before, storage.all())


class TestUserIntanciateWithAgs(unittest.TestCase):
    """Class for testing instanciation of a User with args"""

    def test_args_instantiates(self):
        """Test that a completely new instance is created when *args is given
        despite of the values in args."""
        args = (str(uuid.uuid4()), datetime.now(), datetime.now())
        instance = User(*args)
        self.assertNotEqual(instance.id, args[0])
        self.assertNotEqual(instance.created_at, args[1])
        self.assertNotEqual(instance.updated_at, args[2])

    def test_instantiation_with_single_integer(self):
        """Test instanciation with a single value"""
        instance = User(1)
        self.assertIsInstance(instance.id, str)
        self.assertIsInstance(instance.created_at, datetime)
        self.assertIsInstance(instance.updated_at, datetime)


class TestUserWithKwargs(unittest.TestCase):
    """Class for testing initialization of User with kwargs"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = User()
        self.instance.first_name = 'Brian'
        self.instance.last_name = 'Kim'
        self.instance.email = 'one@main.com'
        self.instance.password = '1234'
        self.kwargs = self.instance.to_dict()
        self.new = User(**self.kwargs)

    def tearDown(self):
        """Return public class attributes to empty strings"""
        User.first_name = ""
        User.last_name = ""
        User.email = ""
        User.password = ""

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
            User(**self.kwargs)
        self.kwargs['created_at'] = '12:00:00'
        with self.assertRaises(ValueError):
            User(**self.kwargs)

    def test_updated_at_not_iso_format(self):
        """Test that an error occurs when the updated_at value is not
        an iso formatted string"""
        self.kwargs['updated_at'] = datetime.now()
        with self.assertRaises(TypeError):
            User(**self.kwargs)
        self.kwargs['updated_at'] = '12:00:00'
        with self.assertRaises(ValueError):
            User(**self.kwargs)

    def test_id_not_uuid4(self):
        """Test that no error occurs when id in kwargs is not of type
        uuid4."""
        self.kwargs['id'] = '123'
        self.assertTrue(User(**self.kwargs))
        self.kwargs['id'] = 123
        self.assertTrue(User(**self.kwargs))

    def test_empty_kwargs(self):
        """Test that an empty kwargs causes new instance to be creates"""
        self.kwargs = {}
        objects_before = storage.all().copy()
        User(**self.kwargs)
        self.assertTrue(objects_before != storage.all())

    def test_kwargs_missing_one_attribute(self):
        """Test that a kwargs missing an attribute doesn't cause new object
        creation"""
        del self.kwargs['id']
        new_instance = User(**self.kwargs)
        with self.assertRaises(AttributeError):
            new_instance.id

    def test_new_instance_is_not_original(self):
        """Test that an instance loaded from anothers dictionary is not
        identical to the original"""
        self.assertFalse(self.instance is self.new)


class TestUserWithArgsAndKwargs(unittest.TestCase):
    """Class for testing instantiation with both args and kwargs"""

    def setUp(self):
        """Setup instance to be used in testing"""
        self.instance = User()
        self.kwargs = self.instance.to_dict()
        self.args = (uuid.uuid4(), datetime.now(), datetime.now())

    def test_args_and_kwargs_instanciates(self):
        """Test that kwargs is used instead of args in instanciation."""
        new_instance = User(*self.args, **self.kwargs)
        self.assertEqual(self.instance.__dict__, new_instance.__dict__)

    def test_no_new_object_is_created(self):
        """Test that a new object is not added to the objects in storage"""
        before_loading = storage.all().copy()
        User(*self.args, **self.kwargs)
        self.assertTrue(before_loading == storage.all())


class TestUserPublicClassAttributes(unittest.TestCase):
    """Class for testing the public class attributes of User"""

    def setUp(self):
        """Setup instane to be used in testing"""
        self.instance = User()

    def test_all_public_attrs_exist(self):
        """Test that all public attributes have been declared"""

        public_attrs = ['email', 'password', 'first_name', 'last_name']
        for attr in public_attrs:
            self.assertTrue(hasattr(self.instance, attr))

    def test_type_of_public_class_attrs(self):
        """Test that all public attributes are of correct type"""
        self.assertIsInstance(self.instance.email, str)
        self.assertIsInstance(self.instance.password, str)
        self.assertIsInstance(self.instance.first_name, str)
        self.assertIsInstance(self.instance.last_name, str)

    def test_default_value_of_public_attrs(self):
        """Test that all public attributes have been assigned correct
        default values"""
        self.assertEqual(self.instance.email, "")
        self.assertEqual(self.instance.password, "")
        self.assertEqual(self.instance.first_name, "")
        self.assertEqual(self.instance.last_name, "")

    def test_assigning_email(self):
        """Test that assigning email changes it effectively"""
        User.email = 'brian@kim.com'
        self.assertEqual(self.instance.email, 'brian@kim.com')
        self.instance.email = 'new@one.com'
        self.assertEqual(self.instance.email, 'new@one.com')
        User.email = ''

    def test_assigning_password(self):
        """Test that assingning password changes it efectively"""
        User.password = '1234'
        self.assertEqual(self.instance.password, '1234')
        self.instance.password = '5678'
        self.assertEqual(self.instance.password, '5678')
        User.password = ''

    def test_assigning_first_name(self):
        """Test that assigning first_name changes it effectively"""
        User.first_name = 'Brian'
        self.assertEqual(self.instance.first_name, 'Brian')
        self.instance.first_name = 'Kim'
        self.assertEqual(self.instance.first_name, 'Kim')
        User.first_name = ''

    def test_assigning_last_name(self):
        """Test that assigning last_name changes it effectively"""
        User.last_name = 'Kim'
        self.assertEqual(self.instance.last_name, 'Kim')
        self.instance.last_name = 'Brian'
        self.assertEqual(self.instance.last_name, 'Brian')
        User.last_name = ''


class TestUserStrMethod(unittest.TestCase):
    """Class for testing the __str__ method """

    def test_str_representation(self):
        """Test that the str representation of the User instance is
        formatted correctly"""
        instance = User()
        expected = "[{}] ({}) {}".format(
            instance.__class__.__name__, instance.id,
            instance.__dict__)
        self.assertEqual(expected, str(instance))


class TestUserToDictMethod(unittest.TestCase):
    """Class for testing the to_dict method"""

    def setUp(self):
        """Setup variables to be used in tests"""
        self.instance = User()

    def test_value_of_class_key(self):
        """Test that the __class__ key has the correct class name ie. User"""
        self.assertEqual(self.instance.to_dict()['__class__'], 'User')


if __name__ == '__main__':
    unittest.main()
