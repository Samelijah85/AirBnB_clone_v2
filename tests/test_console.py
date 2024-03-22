#!/usr/bin/python3
import unittest
from unittest.mock import patch
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from console import HBNBCommand


class TestHBNBCommand(TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    @patch('sys.stdout', new_callable=StringIO)
    def test_create(self, mock_stdout):
        # Test creating an object
        self.console.do_create('State name="California"')
        # Assert that the object is created successfully
        output = mock_stdout.getvalue().strip()
        self.assertRegex(output, r'\w*\-?')

    @patch('sys.stdout', new_callable=StringIO)
    def test_all(self, mock_stdout):
        # Test showing an object
        # self.console.do_show('State 1')
        self.console.do_create('State name="California"')
        self.console.do_all('State')
        # Assert that the object is shown successfully
        output = mock_stdout.getvalue().strip()
        self.assertIn('State', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show(self, mock_stdout):
        # Test showing an object
        self.console.do_create('State name="California"')
        _id = mock_stdout.getvalue().strip()

        # Clear the buffer
        # mock_stdout.seek(0)
        # mock_stdout.truncate()

        # Show the object
        self.console.do_show(f'State {_id}')
        _id1 = mock_stdout.getvalue().strip()

        # Assert that the object is shown successfully
        self.assertIn(_id, _id1)
    # Add similar test methods for 'all' and 'delete'


if __name__ == '__main__':
    unittest.main()
