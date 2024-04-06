"""This module contains the job definitions for the application."""

from .extensions import scheduler


@scheduler.task("interval", id="my_job", seconds=10)
def my_job():
    """Sample job that prints to the console."""
    print("This job is executed every 10 seconds.")
