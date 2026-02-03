from app.db import get_db
from app.services import create_task, list_tasks, toggle_task_done


def test_toggle_done_affects_filters(app):
    with app.app_context():
        db = get_db()
        t1 = create_task(db, text="first")
        t2 = create_task(db, text="second")

        toggle_task_done(db, task_id=t1.id)

        done_ids = [t.id for t in list_tasks(db, filter_name="done")]
        active_ids = [t.id for t in list_tasks(db, filter_name="active")]

    assert done_ids == [t1.id]
    assert active_ids == [t2.id]
