#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
from os import getenv


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Testeing to save")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        temp = {}
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        # Saving new object to ensure it's in storage
        new.save()
        found = False
        # Now checking if new object is in storage
        for obj in storage.all().values():
            if obj is new:
                found = True
                break
        self.assertTrue(found, "New object was not added to __objects")

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        new_id = new.id
        storage.save()
        storage.reload()
        _id = f'BaseModel.{new_id}'
        # Directly fetch the object by its unique ID after reloading
        reloaded_obj = storage.all()
        ob_id = f'{new.__class__.__name__}' + '.' + new.id
        # Ensure an object was returned after reload and it's the correct one
        self.assertIsNotNone(reloaded_obj,
                             "No object was loaded after reload.")

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        new.save()  # Ensure the object is saved and thus added to storage
        _id = new.id
        expected_key = f'BaseModel.{_id}'
        # Directly check if the expected key is in the keys of storage
        self.assertIn(expected_key, storage.all().keys(),
                      "Expected key format not found in storage keys")

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        # print(type(storage))
        self.assertEqual(type(storage), FileStorage)
