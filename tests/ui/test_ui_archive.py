from app.db import get_db
from app.services import list_tasks


def test_ui_archive_button_moves_task_to_archived(client, app):
    client.post("/tasks", data={"text": "archive this"}, follow_redirects=True)

    with app.app_context():
        db = get_db()
        task_id = list_tasks(db, filter_name="all")[0].id

    res = client.post(f"/tasks/{task_id}/archive", follow_redirects=True)
    assert res.status_code == 200

    # After redirect back to All, task should be gone.
    assert b"archive this" not in res.data

    res = client.get("/?filter=archived")
    assert res.status_code == 200
    assert b"archive this" in res.data


def test_ui_archive_done_archives_done_tasks_only(client, app):
    client.post("/tasks", data={"text": "task-a"}, follow_redirects=True)
    client.post("/tasks", data={"text": "task-b"}, follow_redirects=True)

    with app.app_context():
        db = get_db()
        tasks = list_tasks(db, filter_name="all")
        id_a = next(t.id for t in tasks if t.text == "task-a")

    client.post(f"/tasks/{id_a}/toggle", follow_redirects=True)
    res = client.post("/tasks/archive_done", follow_redirects=True)
    assert res.status_code == 200

    res = client.get("/?filter=archived")
    assert b"task-a" in res.data
    assert b"task-b" not in res.data

    res = client.get("/?filter=active")
    assert b"task-b" in res.data
