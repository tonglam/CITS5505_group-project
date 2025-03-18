"""This module is used to run all tests in the tests directory."""

import unittest

from flask import Flask

from app import create_app

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
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestApi))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAuth))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCommunity))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPopular))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPost))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSearch))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUser))
    return suite


def api_suite():
    """Return the api test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestApi))
    return suite


def auth_suite():
    """Return the auth test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAuth))
    return suite


def community_suite():
    """Return the community test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCommunity))
    return suite


def popular_suite():
    """Return the popular test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPopular))
    return suite


def post_suite():
    """Return the post test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPost))
    return suite


def search_suite():
    """Return the search test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSearch))
    return suite


def user_suite():
    """Return the user test suite."""

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUser))
    return suite


def set_up_end2end_app() -> Flask:
    """Set up the end to end test case."""

    print("\nCreating end to end test instance.")

    app = create_app()
    app.config["FLASK_ENV"] = "test"
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    return app
