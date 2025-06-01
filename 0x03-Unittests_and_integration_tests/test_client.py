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

from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from utils import get_json  # for patching
import unittest


class TestGithubOrgClient(unittest.TestCase):

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method returns correct repo names."""

        # Fake payload returned by get_json
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos

        # Patch _public_repos_url as a property returning a fake URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Expect list of repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Confirm both were called once
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
            mock_repos_url.assert_called_once()
