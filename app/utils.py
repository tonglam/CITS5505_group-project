"""Utility functions for the application."""

import configparser
import logging
import os
import uuid
from datetime import datetime, timezone

from app.constants import EnvironmentEnum


def load_config() -> configparser.ConfigParser:
    """Function to load config.ini file."""
    config = configparser.ConfigParser()

    environment = get_env()
    config_file = f"config.{environment}.ini"

    if not os.path.exists(config_file):
        config_file = "config.ini"

    logging.info("Loading config file: %s", config_file)

    config.read(config_file)
    return config


def get_env() -> str:
    """Function to get environment."""
    return os.environ.get("FLASK_ENV", EnvironmentEnum.DEV.value)


def get_config(section, key) -> str:
    """Function to get config value from config.ini file."""
    return load_config()[section][key]


def generate_uuid() -> str:
    """Function to generate UUID."""
    return str(uuid.uuid4())


def generate_time() -> datetime:
    """Function to generate current time."""
    return datetime.now(tz=timezone.utc)


def generate_date() -> str:
    """Function to generate current date."""
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")


def calculate_render_page(current_page: int, total_pages: int) -> tuple:
    """Function to calculate render page.
    Returns a tuple containing the first and last page numbers to be rendered"""

    if total_pages <= 5:
        return 1, total_pages

    if current_page <= 3:
        return 1, 5

    if current_page >= total_pages - 2:
        return total_pages - 4, total_pages

    return current_page - 2, current_page + 2


def get_pagination_details(
    current_page: int, total_pages: int, total_items: int
) -> dict:
    """Function to get pagination details."""

    first_page, last_page = calculate_render_page(current_page, total_pages)

    return {
        "first_page": first_page,
        "last_page": last_page,
        "current_page": current_page,
        "previous_page": current_page - 1 if current_page > 1 else 1,
        "next_page": current_page + 1 if current_page < total_pages else total_pages,
        "total_pages": total_pages,
        "total_items": total_items,
    }


def format_datetime_to_readable_string(dt):
    """Function to format datetime to readable string."""

    def day_suffix(day):
        return (
            "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        )

    return dt.strftime(f"%d{day_suffix(dt.day)} %B %Y").lstrip('0')


def format_datetime_to_local_date_diff(dt):
    """Function to format datetime to local date difference."""

    local_dt = dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    today = datetime.now().date()
    date_diff = today - local_dt.date()
    diff = date_diff.days

    if diff == 0:
        return "today"

    if diff > 0:
        return f"{diff} days ago"

    return f"in {-diff} days"
