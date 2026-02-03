from __future__ import annotations

from flask import Blueprint, jsonify, request

from .db import get_db
from .services import ValidationError, create_task, list_tasks, tasks_to_dicts

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
    return jsonify(task.__dict__), 201
