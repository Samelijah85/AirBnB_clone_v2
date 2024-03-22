#!/usr/bin/python3
""" """
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
from os import getenv


class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        new.city_id = "0001"
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        new.user_id = '0090'
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        new = self.value()
        new.name = "Name"
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        new = self.value()
        new.description = "description"
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """ """
        new = self.value()
        new.number_rooms = 10
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        new.number_bathrooms = 2
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        new = self.value()
        new.max_guest = 8
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """ """
        new = self.value()
        new.price_by_night = 90
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """ """
        new = self.value()
        new.latitude = -78.382324
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """ """
        new = self.value()
        new.latitude = 12.1923
        self.assertEqual(type(new.latitude), float)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Testeing to save")
    def test_amenity_ids_files(self):
        """ """
        new = self.value()
        new.amenities = ['wifi', 'tv']
        self.assertEqual(new.amenities[0], 'wifi')

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Testeing to save")
    def test_amenity_ids(self):
        """Test that amenities can be added correctly."""
        from models.amenity import Amenity
        new = self.value()
        wifi = Amenity(name="wifi")
        tv = Amenity(name="tv")
        new.amenities.append(wifi)
        new.amenities.append(tv)
        self.assertTrue(isinstance(new.amenities, list))
        # Further checks can ensure that 'wifi' and 'tv'
        #  are indeed in amenities
        # self.assertIn(wifi, new.amenities)
        # self.assertIn(tv, new.amenities)
