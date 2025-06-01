#!/usr/bin/env python3
"""
Test suite for client.GithubOrgClient class.
"""

import sys
import os
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
import requests

# Fix import errors
sys.path.insert(0, os.path.abspath('.'))

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient unit tests."""

    # ... (keep all your existing unit tests here) ...

@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient integration tests."""

    @classmethod
    def setUpClass(cls):
        """Set up class with mock for requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect for requests.get mock."""
            if url == "https://api.github.com/orgs/google":
                return cls.mock_response(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return cls.mock_response(cls.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    @classmethod
    def mock_response(cls, payload):
        """Create a mock response with given payload."""
        response = unittest.mock.Mock()
        response.json.return_value = payload
        return response

    def test_public_repos(self):
        """Test public_repos method without license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)