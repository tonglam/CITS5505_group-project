"""This is the test suite for the application."""

import os
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

suite_functions = {
    "api": api_suite,
    "auth": auth_suite,
    "community": community_suite,
    "notice": notice_suite,
    "popular": popular_suite,
    "post": post_suite,
    "search": search_suite,
    "user": user_suite,
}


def run_suite(name=None) -> None:
    """Run a specific test suite or all suites."""

    if name:
        suite_function = suite_functions.get(name)
        if not suite_function:
            print(f"Invalid argument: {name}")
            print("Usage: python test.py [api|auth|...]")
            sys.exit(1)
        suite = suite_function()
    else:
        suite = suites()

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print("Test failed.")
        # remove the test database
        db_file = "instance/requestForum.test.sqlite"
        if os.path.exists(db_file):
            os.remove(db_file)
            print("Removed the test database.")

        sys.exit(1)
    print("Test passed.")


if __name__ == "__main__":
    argNum = len(sys.argv)

    if argNum > 2:
        print("Usage: python test.py [api|auth|...]")
        sys.exit(1)
    elif argNum == 2:
        suite_name = sys.argv[1]
        print(f"Testing the {suite_name} module.")
        run_suite(suite_name)
    else:
        print("Testing all modules.")
        run_suite()
