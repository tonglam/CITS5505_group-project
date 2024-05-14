"""This module is used to run all tests in the tests directory."""

import unittest

from .test_api import TestApi
from .test_auth import TestAuth
from .test_community import TestCommunity
from .test_popular import TestPopular
from .test_post import TestPost
from .test_search import TestSearch
from .test_user import TestUser


def suites():
    """Return all test suites."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestApi))
    suite.addTest(unittest.makeSuite(TestAuth))
    suite.addTest(unittest.makeSuite(TestCommunity))
    suite.addTest(unittest.makeSuite(TestPopular))
    suite.addTest(unittest.makeSuite(TestPost))
    suite.addTest(unittest.makeSuite(TestSearch))
    suite.addTest(unittest.makeSuite(TestUser))
    return suite


def api_suite():
    """Return the api test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestApi))
    return suite


def auth_suite():
    """Return the auth test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAuth))
    return suite


def community_suite():
    """Return the community test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommunity))
    return suite


def popular_suite():
    """Return the popular test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPopular))
    return suite


def post_suite():
    """Return the post test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPost))
    return suite


def search_suite():
    """Return the search test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSearch))
    return suite


def user_suite():
    """Return the user test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUser))
    return suite
