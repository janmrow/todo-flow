import pytest

from app.services import MAX_TASK_LEN, ValidationError, validate_task_text


def test_validate_task_text_trims_whitespace():
    assert validate_task_text("  hello  ") == "hello"


def test_validate_task_text_rejects_empty():
    with pytest.raises(ValidationError):
        validate_task_text("   ")


def test_validate_task_text_rejects_too_long():
    with pytest.raises(ValidationError):
        validate_task_text("x" * (MAX_TASK_LEN + 1))
