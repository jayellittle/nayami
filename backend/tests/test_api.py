import requests


BASE_URL = "http://localhost:8000"

def test_create_post():
    response = requests.post(
        f"{BASE_URL}/posts", 
        json={"content": "Test post"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

if __name__ == "__main__":
    test_create_post()
    test_get_posts()
    print("All tests passed!")
