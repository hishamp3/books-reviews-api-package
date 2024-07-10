from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json()["message"] == "success"


def test_get_book(book_id):
    response = client.get("/books/"+str(book_id))
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()["title"] == "Sherlock Holmes"


if __name__ == "__main__":
    test_get_all_books()
    test_get_book(2)
