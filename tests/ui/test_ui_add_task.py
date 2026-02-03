def test_ui_add_task_shows_on_list(client):
    res = client.post("/tasks", data={"text": "do laundry"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"do laundry" in res.data


def test_ui_add_empty_task_shows_flash_error(client):
    res = client.post("/tasks", data={"text": "   "}, follow_redirects=True)
    assert res.status_code == 200
    assert b"cannot be empty" in res.data.lower()
