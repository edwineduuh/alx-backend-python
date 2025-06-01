#!/usr/bin/env python3
"""
Test suite for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # Adjust import if your path differs


class TestGithubOrgClient(unittest.TestCase):


    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        # Setup mock to not call the real get_json
        mock_get_json.return_value = {"key": "value"}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, mock_get_json.return_value)
