from app.db import get_db
from app.services import list_tasks


def test_ui_delete_archived_task_removes_it(client, app):
    client.post("/tasks", data={"text": "trash"}, follow_redirects=True)

    with app.app_context():
        db = get_db()
        task_id = list_tasks(db, filter_name="all")[0].id

    client.post(f"/tasks/{task_id}/archive", follow_redirects=True)

    res = client.post(f"/tasks/{task_id}/delete?filter=archived", follow_redirects=True)
    assert res.status_code == 200
    assert b"Task deleted." in res.data

    res = client.get("/?filter=archived")
    assert b"trash" not in res.data
