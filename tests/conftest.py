import sys
from pathlib import Path

# ruff: noqa: E402
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest

from app import create_app
from app.db import init_db


@pytest.fixture()
def app(tmp_path):
    app = create_app("test")
    app.config.update(
        DATABASE_PATH=str(tmp_path / "test.sqlite"),
        SECRET_KEY="test",
    )
    with app.app_context():
        init_db()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
