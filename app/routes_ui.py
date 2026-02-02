from __future__ import annotations

from flask import Blueprint

bp = Blueprint("ui", __name__)


@bp.get("/")
def index():
    return "One-Line To-Do"
