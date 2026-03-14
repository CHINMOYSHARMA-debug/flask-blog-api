def test_register(client):
    
    res = client.post("/register", json={
        "username": "john",
        "email": "john@test.com",
        "password": "123456"
    })

    assert res.status_code == 201

def test_login(client):

    client.post("/register", json={
        "username": "john",
        "email": "john@test.com",
        "password": "123456"
    })

    res = client.post("/login", json={
        "username": "john",
        "password": "123456"
    })

    assert res.status_code == 200
    assert "access_token" in res.json["data"]
