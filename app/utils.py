"""Utility functions for the application."""

import configparser
import logging
import os
import uuid
from datetime import datetime


def load_config() -> configparser.ConfigParser:
    """Function to load config.ini file."""
    config = configparser.ConfigParser()

    environment = os.environ.get("FLASK_ENV", "dev")
    config_file = f"config_{environment}.ini"

    if not os.path.exists(config_file):
        config_file = "config.ini"

    logging.info("Loading config file: %s", config_file)

    config.read(config_file)
    return config


def get_config(section, key) -> str:
    """Function to get config value from config.ini file."""
    return load_config()[section][key]


def generate_uuid() -> str:
    """Function to generate UUID."""
    return str(uuid.uuid4())


def generate_time() -> datetime:
    """Function to generate current time."""
    return datetime.now()


def generate_date() -> str:
    """Function to generate current date."""
    return datetime.now().strftime("%Y-%m-%d")
