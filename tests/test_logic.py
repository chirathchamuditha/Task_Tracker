"""Unit tests for logic.py.

These run in the pipeline. If any assertion fails, the pipeline turns red
and the Docker image is never built or published.
"""
import pytest

from logic import (
    make_task,
    normalize_priority,
    sort_tasks,
    summarize,
    validate_title,
)


def test_normalize_priority_accepts_valid_values():
    assert normalize_priority("high") == "high"
    assert normalize_priority("LOW") == "low"
    assert normalize_priority("  medium  ") == "medium"


def test_normalize_priority_falls_back_to_default():
    assert normalize_priority(None) == "medium"
    assert normalize_priority("urgent") == "medium"
    assert normalize_priority("") == "medium"


def test_validate_title_trims_whitespace():
    assert validate_title("  buy milk  ") == "buy milk"


def test_validate_title_rejects_empty():
    with pytest.raises(ValueError):
        validate_title("   ")
    with pytest.raises(ValueError):
        validate_title(None)


def test_validate_title_rejects_too_long():
    with pytest.raises(ValueError):
        validate_title("x" * 101)


def test_make_task_has_expected_shape():
    task = make_task(1, "Write tests", "high")
    assert task == {"id": 1, "title": "Write tests", "priority": "high", "done": False}


def test_sort_tasks_puts_unfinished_and_urgent_first():
    tasks = [
        {"id": 1, "title": "a", "priority": "low", "done": False},
        {"id": 2, "title": "b", "priority": "high", "done": False},
        {"id": 3, "title": "c", "priority": "high", "done": True},
    ]
    ordered = [t["id"] for t in sort_tasks(tasks)]
    # id 2 (high, not done) first, then id 1 (low, not done), then done task
    assert ordered == [2, 1, 3]


def test_summarize_counts_correctly():
    tasks = [
        {"id": 1, "title": "a", "priority": "low", "done": True},
        {"id": 2, "title": "b", "priority": "low", "done": False},
    ]
    assert summarize(tasks) == {"total": 2, "done": 1, "remaining": 1}


def test_summarize_handles_empty_list():
    assert summarize([]) == {"total": 0, "done": 0, "remaining": 0}
