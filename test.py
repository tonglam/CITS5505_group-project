"""This is the test suite for the application."""

import sys
import unittest

from tests import (
    api_suite,
    auth_suite,
    community_suite,
    notice_suite,
    popular_suite,
    post_suite,
    search_suite,
    suites,
    user_suite,
)


def run():
    """Run the test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites())


def api():
    """Run the api test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(api_suite())


def auth():
    """Run the auth test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(auth_suite())


def community():
    """Run the community test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(community_suite())


def notice():
    """Run the notice test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(notice_suite())


def popular():
    """Run the popular test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(popular_suite())


def post():
    """Run the post test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(post_suite())


def search():
    """Run the search test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(search_suite())


def user():
    """Run the user test suite."""

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(user_suite())


if __name__ == "__main__":
    argNum = len(sys.argv)

    if argNum < 1 or argNum > 2:
        print("No argument provided. Usage: python test.py [api|auth|...]")
    elif argNum == 1:
        print("Testing all modules.")
        run()
    else:
        module = sys.argv[1]

        if module == "api":
            print("Testing the api module.")
            api()
        elif module == "auth":
            print("Testing the auth module.")
            auth()
        elif module == "community":
            print("Testing the community module.")
            community()
        elif module == "notice":
            print("Testing the notice module.")
            notice()
        elif module == "popular":
            print("Testing the popular module.")
            popular()
        elif module == "post":
            print("Testing the post module.")
            post()
        elif module == "search":
            print("Testing the search module.")
            search()
        elif module == "user":
            print("Testing the user module.")
            user()
        else:
            print(f"Invalid argument: {module}")
            print("Usage: python test.py [api|auth|...]")
