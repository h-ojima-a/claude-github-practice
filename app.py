from flask import Flask, jsonify, request

app = Flask(__name__)

todos = {}
next_id = 1


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(list(todos.values())), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    todo = {"id": next_id, "title": data["title"], "done": False}
    todos[next_id] = todo
    next_id += 1
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "todo not found"}), 404
    data = request.get_json()
    title = data.get("title")
    if not title or not title.strip():
        return jsonify({"error": "title is required"}), 400
    todos[todo_id]["title"] = title.strip()
    return jsonify(todos[todo_id]), 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todos.pop(todo_id, None)
    return "", 204


@app.route("/todos/search", methods=["GET"])
def search_todos():
    keyword = request.args.get("keyword")
    if not keyword or not keyword.strip():
        return jsonify({"error": "keyword parameter is required"}), 400
    kw = keyword.strip().lower()
    results = [t for t in todos.values() if kw in t["title"].lower()]
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=True)
