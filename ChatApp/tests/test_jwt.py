import uuid

def get_token(client):
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "test1234"

    client.post("/register", json={
        "username": username,
        "password": password
    })

    res = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert res.status_code == 200
    return res.json()["access_token"]



def test_access_protected_route_with_token(client):
    token = get_token(client)

    response = client.get(
        "/chatrooms/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_access_protected_route_without_token(client):
    response = client.get("/chatrooms/")
    assert response.status_code in (401, 403)


def test_access_with_invalid_token(client):
    response = client.get(
        "/chatrooms/",
        headers={"Authorization": "Bearer invalid.token.value"}
    )

    assert response.status_code in (401, 403)
