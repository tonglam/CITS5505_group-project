"""Utility functions for the application."""

import configparser
import uuid
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini")


def get_config(section, key) -> str:
    """Function to get config value from config.ini file."""
    return config[section][key]


def generate_uuid() -> str:
    """Function to generate UUID."""
    return str(uuid.uuid4())


def generate_time() -> datetime:
    """Function to generate current time."""
    return datetime.now()


def generate_date() -> str:
    """Function to generate current date."""
    return datetime.now().strftime("%Y-%m-%d")
