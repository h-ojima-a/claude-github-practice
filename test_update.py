import pytest
from app import app, todos
import app as app_module


@pytest.fixture(autouse=True)
def reset_state():
    todos.clear()
    app_module.next_id = 1


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_update_todo_title(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.put("/todos/1", json={"title": "Buy oat milk"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["title"] == "Buy oat milk"
    assert data["done"] is False


def test_update_todo_not_found(client):
    response = client.put("/todos/999", json={"title": "Buy milk"})
    assert response.status_code == 404


def test_update_todo_missing_title(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.put("/todos/1", json={})
    assert response.status_code == 400


def test_update_todo_empty_title(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.put("/todos/1", json={"title": ""})
    assert response.status_code == 400


def test_update_todo_whitespace_only_title(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.put("/todos/1", json={"title": "   "})
    assert response.status_code == 400


def test_update_todo_strips_whitespace(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.put("/todos/1", json={"title": "  Buy oat milk  "})
    assert response.status_code == 200
    assert response.get_json()["title"] == "Buy oat milk"


def test_update_todo_no_body(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.put("/todos/1", content_type="application/json")
    assert response.status_code == 400


def test_update_todo_persists(client):
    client.post("/todos", json={"title": "Buy milk"})
    client.put("/todos/1", json={"title": "Buy oat milk"})

    response = client.get("/todos")
    titles = [t["title"] for t in response.get_json()]
    assert "Buy oat milk" in titles
    assert "Buy milk" not in titles
