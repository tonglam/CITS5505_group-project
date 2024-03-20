"""This file is used to run the application."""

import os
import sys

from app import create_app

# from app.extensions import scheduler

# Get the directory of the current file (run.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (which contains the 'app' directory) to sys.path
app_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(app_dir)

app = create_app()


if __name__ == "__main__":
    # scheduler.start()
    app.run(debug=True)
