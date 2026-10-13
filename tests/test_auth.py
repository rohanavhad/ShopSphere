def test_register_and_me(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com", "full_name": "Test User", "password": "safe-password-123"
    })
    assert response.status_code == 201
    token = response.json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "test@example.com"

def test_duplicate_email_rejected(client):
    payload = {"email":"same@example.com","full_name":"Test User","password":"safe-password-123"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 400
