"""Pure Business logic for the task tracker.

Everything here in plain Python with noFlask and no global state, which
makes it easy to test. The web layer in app.py calls in to these function.

"""
PRIORITIES = {"low": 1, "medium": 2, "high": 3}
DEFAULT_PRIORITY = "medium"
MAX_TITLE_LENGTH = 100

def normalize_priority(value):
    """
    Retun a valid priority string, falling back to the default
    """
    if value is None:
        return DEFAULT_PRIORITY
    cleaned = str(value).strip().lower()
    return cleaned if cleaned in PRIORITIES else DEFAULT_PRIORITY


def validate_title(title):
    """
    Return a cleaned title or raise ValueError if it is not usable
    """
    if title is None:
        raise ValueError("Title is required")
    cleaned = str(title).strip()
    if not cleaned:
        raise ValueError("Title cannot be empty")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title must be {MAX_TITLE_LENGTH} characters or fewer.")
    return cleaned


def make_task(task_id, title, priority=DEFAULT_PRIORITY):
    """
    Build a task task dictionary from raw input
    """
    return {
        "id": task_id,
        "title": title,
        "priority": normalize_priority(priority),
        "done": False

    }

def priority_rank(task):
    """
    Numeric urgency of a task, used for sorting.
    """
    return PRIORITIES.get(task["priority"], PRIORITIES[DEFAULT_PRIORITY])

def sort_tasks(tasks):
    """
    Unfinished tasks first, then most urgent, then oldest first
    """
    return sorted(tasks, key=lambda t: (t["done"], -priority_rank(t), t["id"]))


def summarize(tasks):
    """Return simple counts about a list of tasks """

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])

    return {"total": total, "done": done, "remaining": total-done}