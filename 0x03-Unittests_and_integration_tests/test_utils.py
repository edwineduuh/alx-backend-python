#!/usr/bin/env python3
from parameterized import parameterized
import unittest
from utils import access_nested_map  # adjust if your import path differs

class TestAccessNestedMap(unittest.TestCase):
    # Existing test method for successful accesses (you probably already have this)
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # New method to test exceptions for missing keys
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Check that the exception message matches the missing key (the last key in path)
        self.assertEqual(str(context.exception), repr(path[-1]))

# import unittest
# from parameterized import parameterized
# from utils import access_nested_map

# class TestAccessNestedMap(unittest.TestCase):

#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         self.assertEqual(access_nested_map(nested_map, path), expected)
