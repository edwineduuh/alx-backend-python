#!/usr/bin/env python3
"""
Test suite for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')  # If this still fails, change to 'client.utils.get_json'
    def test_org(self, org_name, mock_get_json):
        """Test that .org returns correct data and calls get_json once."""
        expected = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org  # not client.org()

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)


from client import GithubOrgClient
from unittest.mock import patch
import unittest


class TestGithubOrgClient(unittest.TestCase):
    # ... (your other tests)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value from org."""

        # Payload to return when .org is accessed
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])
