"""Script to create the test database."""

import psycopg2

from app.utils import get_config


def create_test_database():
    """Create the test database if it doesn't exist."""
    # Get the main database URL
    db_url = get_config("POSTGRESQL", "DATABASE_URL")

    # Parse the URL to get connection details
    # Format: postgresql://user:password@host/dbname
    db_url = db_url.replace("postgresql://", "")
    user_pass, host_db = db_url.split("@")
    user, password = user_pass.split(":")
    host, dbname = host_db.split("/")

    # Connect to the default database to create the test database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            # Create the test database if it doesn't exist
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s", (dbname + "_test",)
            )
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {dbname}_test")
                print(f"Created test database: {dbname}_test")
            else:
                print(f"Test database {dbname}_test already exists")
    finally:
        conn.close()


if __name__ == "__main__":
    create_test_database()
