import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_search_todos_by_title(client):
    client.post("/todos", json={"title": "Buy milk"})
    client.post("/todos", json={"title": "Buy eggs"})
    client.post("/todos", json={"title": "Read book"})

    response = client.get("/todos/search?q=Buy")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    titles = [item["title"] for item in data]
    assert "Buy milk" in titles
    assert "Buy eggs" in titles


def test_search_todos_no_results(client):
    client.post("/todos", json={"title": "Buy milk"})

    response = client.get("/todos/search?q=xyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_search_todos_missing_query(client):
    response = client.get("/todos/search")
    assert response.status_code == 400
