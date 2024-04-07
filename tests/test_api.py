"""Tests for the API module."""

import unittest

from tests.config import TestBase


class TestApi(TestBase):
    """This class contains the test cases for the API module."""

    def test_api(self, _, client):
        """Test the API."""
        print("Test the API")


if __name__ == "__main__":
    unittest.main()
