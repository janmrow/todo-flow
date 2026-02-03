from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable

import sqlite3

MAX_TASK_LEN = 200


class ValidationError(ValueError):
    pass


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def validate_task_text(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValidationError("Task text cannot be empty.")
    if len(cleaned) > MAX_TASK_LEN:
        raise ValidationError(f"Task text is too long (max {MAX_TASK_LEN}).")
    return cleaned


@dataclass(frozen=True)
class Task:
    id: int
    text: str
    done: bool
    archived: bool
    created_at: str
    updated_at: str


def _row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=row["id"],
        text=row["text"],
        done=bool(row["done"]),
        archived=bool(row["archived"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def create_task(db: sqlite3.Connection, text: str) -> Task:
    cleaned = validate_task_text(text)
    now = utc_now_iso()

    cur = db.execute(
        """
        INSERT INTO tasks (text, done, archived, created_at, updated_at)
        VALUES (?, 0, 0, ?, ?)
        """,
        (cleaned, now, now),
    )
    db.commit()

    task_id = int(cur.lastrowid)
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    assert row is not None
    return _row_to_task(row)

