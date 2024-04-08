# pylint: skip-file

import unittest

from .test_api import TestApi
from .test_auth import TestAuth
from .test_community import TestCommunity
from .test_notice import TestNotice
from .test_popular import TestPopular
from .test_post import TestPost
from .test_search import TestSearch
from .test_user import TestUser


def suites():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestApi))
    suite.addTest(unittest.makeSuite(TestAuth))
    suite.addTest(unittest.makeSuite(TestCommunity))
    suite.addTest(unittest.makeSuite(TestNotice))
    suite.addTest(unittest.makeSuite(TestPopular))
    suite.addTest(unittest.makeSuite(TestPost))
    suite.addTest(unittest.makeSuite(TestSearch))
    suite.addTest(unittest.makeSuite(TestUser))
    return suite


def api_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAuth))
    return suite


def auth_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAuth))
    return suite


def community_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommunity))
    return suite


def notice_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNotice))
    return suite


def popular_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPopular))
    return suite


def post_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPost))
    return suite


def search_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSearch))
    return suite


def user_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUser))
    return suite
