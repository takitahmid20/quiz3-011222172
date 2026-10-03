import pytest
from fastapi.testclient import TestClient
from main import app, books

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset():
    books.clear()
    import main
    main.next_id = 1
    yield


def test_create_book():
    response = client.post("/books", json={
        "title": "Clean Code",
        "author": "Robert Martin",
        "price": 29.99
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Clean Code"


def test_delete_book():
    # Step 1: create a book first
    client.post("/books", json={
        "title": "Test",
        "author": "Author",
        "price": 9.99
    })

    # Step 2: delete the book
    response = client.delete("/books/1")
    assert response.status_code == 200

    # Step 3: verify it is gone
    check = client.get("/books")
    assert len(check.json()) == 0
