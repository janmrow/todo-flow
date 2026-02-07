from __future__ import annotations

from playwright.sync_api import expect


def _add_task(page, base_url: str, text: str) -> None:
    page.goto(base_url)
    page.locator("input[name='text']").fill(text)
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Task added.")).to_be_visible()


def test_basic_flow_add_done_archive_delete(page, base_url: str):
    task_text = "e2e: buy milk"

    _add_task(page, base_url, task_text)

    # Mark done.
    row = page.locator("li.list-group-item", has_text=task_text)
    row.get_by_role("button", name="Done").click()
    expect(page.get_by_role("button", name="Undo")).to_be_visible()

    # Filter to Done.
    page.get_by_role("link", name="Done").click()
    expect(page.get_by_text(task_text)).to_be_visible()

    # Archive done (bulk) from non-archived view.
    page.get_by_role("button", name="Archive done").click()
    expect(page.get_by_text("Archived", exact=False)).to_be_visible()

    # In archived filter we should see the task.
    page.get_by_role("link", name="Archived").click()
    expect(page.get_by_text(task_text)).to_be_visible()

    # Delete archived task.
    row = page.locator("li.list-group-item", has_text=task_text)
    row.get_by_role("button", name="Delete").click()
    expect(page.get_by_text("Task deleted.")).to_be_visible()
    expect(page.locator("li.list-group-item", has_text=task_text)).to_have_count(0)


def test_empty_task_shows_validation_message(page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Task text cannot be empty.")).to_be_visible()
