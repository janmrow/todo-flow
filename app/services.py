from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable

import sqlite3

MAX_TASK_LEN = 200


class ValidationError(ValueError):
    pass


class NotFoundError(LookupError):
    pass


class StateConflictError(RuntimeError):
    pass


def utc_now_iso() -> str:
    # Keep timestamps stable and easy to compare in tests.
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


def get_task(db: sqlite3.Connection, task_id: int) -> Task | None:
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return None
    return _row_to_task(row)


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
    task = get_task(db, task_id)
    assert task is not None
    return task


def list_tasks(db: sqlite3.Connection, filter_name: str = "all") -> list[Task]:
    filter_name = (filter_name or "all").lower()

    if filter_name == "archived":
        where = "archived = 1"
    elif filter_name == "active":
        where = "archived = 0 AND done = 0"
    elif filter_name == "done":
        where = "archived = 0 AND done = 1"
    elif filter_name == "all":
        where = "archived = 0"
    else:
        raise ValidationError("Unknown filter.")

    rows = db.execute(
        f"SELECT * FROM tasks WHERE {where} ORDER BY created_at DESC, id DESC",
    ).fetchall()
    return [_row_to_task(r) for r in rows]


def tasks_to_dicts(tasks: Iterable[Task]) -> list[dict]:
    return [asdict(t) for t in tasks]


def task_to_dict(task: Task) -> dict:
    return asdict(task)
