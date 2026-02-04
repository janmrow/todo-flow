from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .db import get_db
from .services import (
    NotFoundError,
    StateConflictError,
    ValidationError,
    create_task,
    list_tasks,
    toggle_task_done,
)

bp = Blueprint("ui", __name__)


@bp.get("/")
def index():
    db = get_db()
    filter_name = request.args.get("filter", "all")

    try:
        tasks = list_tasks(db, filter_name=filter_name)
    except ValidationError:
        filter_name = "all"
        tasks = list_tasks(db, filter_name=filter_name)

    return render_template("index.html", tasks=tasks, filter_name=filter_name)


@bp.post("/tasks")
def add_task():
    text = request.form.get("text", "")
    filter_name = request.args.get("filter", "all")

    db = get_db()
    try:
        create_task(db, text=text)
    except ValidationError as e:
        flash(str(e), category="error")
    else:
        flash("Task added.", category="success")

    return redirect(url_for("ui.index", filter=filter_name))


@bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id: int):
    filter_name = request.args.get("filter", "all")
    db = get_db()

    try:
        toggle_task_done(db, task_id=task_id)
    except NotFoundError:
        abort(404)
    except StateConflictError as e:
        flash(str(e), category="error")

    return redirect(url_for("ui.index", filter=filter_name))
