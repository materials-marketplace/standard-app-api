import os
import sqlite3

import databases
import sqlalchemy

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

_DATABASE = None
_ENGINE = None


# Standard approach to enabling foreign key support for sqlite3, however since
# we use the async databases library, we need to use a custom Connection object
# as implemented in the get_database() function below.
# See also: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     print("SET SQLITE PRAGMA")
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


def get_database() -> databases.Database:
    "Get the database connection."
    global _DATABASE, _ENGINE
    if _DATABASE is None:

        # Work-around for sqlite3 due to a limitation in encode/databases
        # and aioqslite: https://github.com/encode/databases/issues/169
        class Connection(sqlite3.Connection):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.execute("PRAGMA foreign_keys=ON")

        _DATABASE = databases.Database(DATABASE_URL, factory=Connection)

        _ENGINE = sqlalchemy.create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )
    return _DATABASE


def get_engine():
    "Get the sqlite 3 engine."
    return _ENGINE
