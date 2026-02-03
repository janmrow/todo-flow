from __future__ import annotations

from flask import Blueprint, render_template, request

from .db import get_db
from .services import ValidationError, list_tasks

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
