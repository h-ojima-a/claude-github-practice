import pytest
from app import app, todos, next_id
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


def test_search_todos_by_keyword(client):
    client.post("/todos", json={"title": "Buy milk"})
    client.post("/todos", json={"title": "Buy eggs"})
    client.post("/todos", json={"title": "Read book"})

    response = client.get("/todos/search?keyword=Buy")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    titles = [item["title"] for item in data]
    assert "Buy milk" in titles
    assert "Buy eggs" in titles


def test_search_todos_case_insensitive(client):
    client.post("/todos", json={"title": "Buy Milk"})
    client.post("/todos", json={"title": "Read book"})

    response = client.get("/todos/search?keyword=buy")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Buy Milk"


def test_search_todos_no_results(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.get("/todos/search?keyword=xyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_search_todos_missing_keyword(client):
    response = client.get("/todos/search")
    assert response.status_code == 400
