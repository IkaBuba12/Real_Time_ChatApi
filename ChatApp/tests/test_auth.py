import uuid

def test_register_user(client):
    username = f"user_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/register",
        json={
            "username": username,
            "password": "test1234"
        }
    )

    assert response.status_code == 200



def test_login_user(client):
    username = "testuser_login"
    password = "test1234"

    client.post("/register", json={
        "username": username,
        "password": password
    })

    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
