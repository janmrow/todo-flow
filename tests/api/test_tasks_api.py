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


def test_api_archive_task_moves_it_out_of_all(client):
    res = client.post("/api/tasks", json={"text": "archive me"})
    task_id = res.get_json()["id"]

    res = client.patch(f"/api/tasks/{task_id}", json={"archived": True})
    assert res.status_code == 200
    assert res.get_json()["archived"] is True

    res = client.get("/api/tasks?filter=all")
    items = res.get_json()["items"]
    assert [t["id"] for t in items] == []

    res = client.get("/api/tasks?filter=archived")
    items = res.get_json()["items"]
    assert [t["id"] for t in items] == [task_id]


def test_api_archive_done_archives_only_done(client):
    t1 = client.post("/api/tasks", json={"text": "a"}).get_json()["id"]
    t2 = client.post("/api/tasks", json={"text": "b"}).get_json()["id"]

    client.patch(f"/api/tasks/{t1}", json={"done": True})

    res = client.post("/api/tasks/archive_done")
    assert res.status_code == 200
    assert res.get_json()["archived_count"] == 1

    res = client.get("/api/tasks?filter=archived")
    items = res.get_json()["items"]
    assert [t["id"] for t in items] == [t1]

    res = client.get("/api/tasks?filter=active")
    items = res.get_json()["items"]
    assert [t["id"] for t in items] == [t2]
