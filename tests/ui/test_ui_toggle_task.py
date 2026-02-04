from app.db import get_db
from app.services import list_tasks


def test_ui_toggle_done_changes_badge_and_button(client, app):
    client.post("/tasks", data={"text": "do laundry"}, follow_redirects=True)

    with app.app_context():
        db = get_db()
        task_id = list_tasks(db, filter_name="all")[0].id

    res = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert res.status_code == 200

    body = res.data.lower()
    assert b"undo" in body
    assert b">done<" in body
