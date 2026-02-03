from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db
from .services import ValidationError, create_task, list_tasks

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
