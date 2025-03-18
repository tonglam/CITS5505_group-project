"""Utility functions for the application."""

import configparser
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

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


def load_env_file() -> dict:
    """Function to load .env file."""
    env_vars = {}
    env_path = Path(".env")

    if env_path.exists():
        with env_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    # Remove quotes if present
                    env_vars[key.strip()] = value.strip().strip("\"'")

    return env_vars


def get_env() -> str:
    """Function to get environment."""
    return os.environ.get("FLASK_ENV", EnvironmentEnum.DEV.value)


def get_config(section, key) -> str:
    """Function to get config value following priority order:
    1. config.ini file
    2. .env file
    3. environment variables
    """
    # Try config file first
    try:
        return load_config()[section][key]
    except (configparser.Error, KeyError):
        pass

    # Try environment variables (both with and without section prefix)
    env_keys = [
        f"{section}_{key}",  # e.g. GOOGLE_OAUTH_CLIENT_ID
        key,  # e.g. OAUTH_CLIENT_ID
    ]

    for env_key in env_keys:
        value = os.environ.get(env_key)
        if value is not None:
            return value

    # If nothing found, raise error
    raise KeyError(
        f"Configuration {section}.{key} not found in config file or environment variables"
    )


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

    return dt.strftime(f"%d{day_suffix(dt.day)} %B %Y").lstrip("0")


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
