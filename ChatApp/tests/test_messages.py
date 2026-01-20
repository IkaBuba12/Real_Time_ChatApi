import uuid

def get_token(client):
    username = f"user_{uuid.uuid4().hex[:8]}"

    client.post("/register", json={
        "username": username,
        "password": "test1234"
    })

    res = client.post(
        "/login",
        data={
            "username": username,
            "password": "test1234"
        }
    )

    print("LOGIN RESPONSE:", res.status_code, res.json())
    return res.json()["access_token"]



def test_create_chatroom(client):
    token = get_token(client)

    response = client.post(
        "/chatrooms/",
        json={"name": "Test Room"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in (200, 201)
    assert "id" in response.json()



def test_send_and_get_messages(client):
    token = get_token(client)

    room = client.post(
        "/chatrooms/",
        json={"name": "Message Room"},
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    room_id = room["id"]

    send = client.post(
        f"/chatrooms/{room_id}/messages",
        json={"content": "Hello World", "room_id": room_id},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert send.status_code == 200

    messages = client.get(
        f"/chatrooms/{room_id}/messages",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert messages.status_code == 200
    assert len(messages.json()) >= 1
    assert messages.json()[0]["content"] == "Hello World"
