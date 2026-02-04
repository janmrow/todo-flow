from app.db import get_db
from app.services import archive_done, archive_task, create_task, list_tasks, toggle_task_done


def test_archive_task_moves_task_to_archived_filter(app):
    with app.app_context():
        db = get_db()
        t1 = create_task(db, text="keep")
        t2 = create_task(db, text="move")

        archive_task(db, task_id=t2.id)

        all_ids = [t.id for t in list_tasks(db, filter_name="all")]
        archived_ids = [t.id for t in list_tasks(db, filter_name="archived")]

    assert all_ids == [t1.id]
    assert archived_ids == [t2.id]


def test_archive_done_archives_only_done_tasks(app):
    with app.app_context():
        db = get_db()
        t1 = create_task(db, text="done one")
        t2 = create_task(db, text="not done")

        toggle_task_done(db, task_id=t1.id)
        count = archive_done(db)

        archived_ids = [t.id for t in list_tasks(db, filter_name="archived")]
        active_ids = [t.id for t in list_tasks(db, filter_name="active")]

    assert count == 1
    assert archived_ids == [t1.id]
    assert active_ids == [t2.id]
