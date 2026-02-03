def test_api_create_and_list_tasks(client):
    res = client.post("/api/tasks", json={"text": "buy milk"})
    assert res.status_code == 201
    task = res.get_json()
    assert task["text"] == "buy milk"
    assert task["done"] is False
    assert task["archived"] is False

    res = client.get("/api/tasks")
    assert res.status_code == 200
    items = res.get_json()["items"]
    assert len(items) == 1
    assert items[0]["text"] == "buy milk"


def test_api_rejects_empty_task_text(client):
    res = client.post("/api/tasks", json={"text": "   "})
    assert res.status_code == 400
    payload = res.get_json()
    assert payload["error"]["code"] == "validation_error"

def test_api_patch_done_updates_task(client):
    res = client.post("/api/tasks", json={"text": "write tests"})
    task_id = res.get_json()["id"]

    res = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True

    res = client.get("/api/tasks?filter=done")
    assert res.status_code == 200
    items = res.get_json()["items"]
    assert [t["id"] for t in items] == [task_id]

    res = client.patch(f"/api/tasks/{task_id}", json={"done": False})
    assert res.status_code == 200
    assert res.get_json()["done"] is False
