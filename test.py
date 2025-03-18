"""This is the test suite for the application."""

import os
import sys
import unittest

from tests import (
    api_suite,
    auth_suite,
    community_suite,
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
    "popular": popular_suite,
    "post": post_suite,
    "search": search_suite,
    "user": user_suite,
}


def cleanup_test_db() -> None:
    """Clean up test database files."""
    db_files = ["instance/requestForum.test.sqlite", "test.db"]
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"Removed test database: {db_file}")
            except OSError as e:
                print(f"Warning: Failed to remove test database {db_file}: {e}")


def run_suite(name=None) -> None:
    """Run a specific test suite or all suites."""
    try:
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
            cleanup_test_db()
            sys.exit(1)

        print("Test passed.")
        cleanup_test_db()

    except (
        unittest.TestCase.failureException,
        unittest.case.TestCase.failureException,
    ) as e:
        print(f"Error running tests: {e}")
        cleanup_test_db()
        sys.exit(1)


if __name__ == "__main__":
    argNum = len(sys.argv)

    if argNum > 2:
        print("Usage: python test.py [api|auth|...|end2end]")
        sys.exit(1)
    elif argNum == 2:
        suite_name = sys.argv[1]
        print(f"Testing the {suite_name} module.")
        run_suite(suite_name)
    else:
        print("Testing all modules.")
        run_suite()
