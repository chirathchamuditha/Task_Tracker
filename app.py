"""Flask web layer

Keeps an in-memory list of tasks (re sets when the server restarts) and exposes a small JSON API 
plus a single html page. All the real rules live in logic.py so they can be tested without starting
a web server.
"""

from flask import Flask, jsonify, render_template, request

from logic import make_task, sort_tasks,summarize

app = Flask(__name__)

_tasks =[]
_next_id = 1

def _seed():
    """ Add a couple of starter tasks so the page isn't empty"""

    global _tasks, _next_id
    _tasks = []
    _next_id = 1

    for title, priority in [
        ("Learn what a CI/CD pipeline is", "high"),
        ("Write a test", "meadium"),
        ("Watch the pipeline go green", "low")
    ]:
        _add(title, priority)


def _add(title, priority):
    global _next_id
    task = make_task(_next_id, title, priority)
    _tasks.append(task)
    _next_id += 1
    return task

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks",methods=["GET"])
def list_task():
    return jsonify({"tasks": sort_tasks(_tasks), "summary": summarize(_tasks)})

@app.route("/api/create", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    try:
        task = _add(data.get("title"), data.get("priority"))
    except ValueError as err:
        return jsonify({"error": str(err)}),400
    return jsonify(task),201

@app.route("/api/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    for task in _tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/health")
def health():
    """Simple check a pipeline or load balancer can ping"""

    return jsonify({"error": "Task not found"}),404

_seed()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
        


