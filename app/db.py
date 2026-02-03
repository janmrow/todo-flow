from __future__ import annotations

import sqlite3

import click
from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """Return a SQLite connection for the current request/app context."""
    db = g.get("db")

    if db is None:
        db = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        db.row_factory = sqlite3.Row
        g.db = db

    return db


def close_db(exception: Exception | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


@click.command("init-db")
def init_db_command() -> None:
    """Initialize the database using schema.sql."""
    init_db()
    click.echo("Initialized the database.")
