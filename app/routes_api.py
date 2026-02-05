from __future__ import annotations

from flask import Blueprint, jsonify, request

from .db import get_db
from .services import (
    NotFoundError,
    StateConflictError,
    ValidationError,
    archive_done,
    create_task,
    delete_task,
    list_tasks,
    set_task_archived,
    set_task_done,
    task_to_dict,
    tasks_to_dicts,
)

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/tasks")
def tasks_list():
    db = get_db()
    filter_name = request.args.get("filter", "all")

    try:
        tasks = list_tasks(db, filter_name=filter_name)
    except ValidationError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 400

    return jsonify({"items": tasks_to_dicts(tasks)})


@bp.post("/tasks")
def tasks_create():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")

    db = get_db()
    try:
        task = create_task(db, text=text)
    except ValidationError as e:
        return jsonify({"error": {"code": "validation_error", "message": str(e)}}), 400

    return jsonify(task_to_dict(task)), 201


@bp.patch("/tasks/<int:task_id>")
def tasks_patch(task_id: int):
    payload = request.get_json(silent=True) or {}

    if "done" not in payload and "archived" not in payload:
        return (
            jsonify(
                {
                    "error": {
                        "code": "validation_error",
                        "message": "Provide at least one field: done or archived",
                    }
                }
            ),
            400,
        )

    db = get_db()
    task = None

    try:
        if "done" in payload:
            done = payload.get("done")
            if not isinstance(done, bool):
                return (
                    jsonify(
                        {
                            "error": {
                                "code": "validation_error",
                                "message": "Field 'done' must be a boolean",
                            }
                        }
                    ),
                    400,
                )
            task = set_task_done(db, task_id=task_id, done=done)

        if "archived" in payload:
            archived = payload.get("archived")
            if not isinstance(archived, bool):
                return (
                    jsonify(
                        {
                            "error": {
                                "code": "validation_error",
                                "message": "Field 'archived' must be a boolean",
                            }
                        }
                    ),
                    400,
                )
            if archived is False:
                return (
                    jsonify(
                        {
                            "error": {
                                "code": "validation_error",
                                "message": "Unarchiving is not supported",
                            }
                        }
                    ),
                    400,
                )
            task = set_task_archived(db, task_id=task_id, archived=True)

    except NotFoundError as e:
        return jsonify({"error": {"code": "not_found", "message": str(e)}}), 404
    except StateConflictError as e:
        return jsonify({"error": {"code": "state_conflict", "message": str(e)}}), 409

    assert task is not None
    return jsonify(task_to_dict(task))


@bp.delete("/tasks/<int:task_id>")
def tasks_delete(task_id: int):
    db = get_db()
    try:
        delete_task(db, task_id=task_id)
    except NotFoundError as e:
        return jsonify({"error": {"code": "not_found", "message": str(e)}}), 404
    except StateConflictError as e:
        return jsonify({"error": {"code": "state_conflict", "message": str(e)}}), 409

    return jsonify({"deleted": True})


@bp.post("/tasks/archive_done")
def tasks_archive_done():
    db = get_db()
    count = archive_done(db)
    return jsonify({"archived_count": count})
