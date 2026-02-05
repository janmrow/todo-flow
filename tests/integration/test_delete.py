from app.db import get_db
from app.services import archive_task, create_task, delete_task, list_tasks


def test_delete_archived_task_removes_it(app):
    with app.app_context():
        db = get_db()
        t = create_task(db, text="to delete")
        archive_task(db, task_id=t.id)

        delete_task(db, task_id=t.id)

        archived = list_tasks(db, filter_name="archived")

    assert archived == []
