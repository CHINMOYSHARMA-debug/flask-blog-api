def test_create_posts(client, token):

    res = client.post(
        "/posts",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Post",
            "content": "Hello world"
        }
    )
    
    assert res.status_code == 201

