"""Tests for the community module."""

import enum

from tests.config import TestBase


class InvalidUpdateEnum(enum.Enum):
    """Enum for invalid Create type."""

    NAME_EMPTY = "Name empty"
    CATEGORY_ID_EMPTY = "Category_id empty"
    DESCRIPTION_EMPTY = "Description empty"


class StatusEnum(enum.Enum):
    """Enum for invalid Update type."""

    SUCCESS = "ok"
    FAIL = "notok"


class TestCommunity(TestBase):
    """This class contains the test cases for the community module."""
