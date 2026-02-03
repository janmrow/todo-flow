from app.db import get_db
from app.services import create_task, list_tasks


def test_create_task_persists_and_is_listed(app):
    with app.app_context():
        db = get_db()
        create_task(db, text="first")
        create_task(db, text="second")

        tasks = list_tasks(db)
        texts = [t.text for t in tasks]

    assert texts == ["second", "first"]
