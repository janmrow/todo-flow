import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402


@pytest.fixture()
def app():
    app = create_app("test")
    app.config.update(SECRET_KEY="test")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
