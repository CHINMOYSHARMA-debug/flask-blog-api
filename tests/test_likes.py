def test_like_post(client, token):

    post = client.post(
        "/posts",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test",
            "content": "Hello"
        }
    )

    assert post.status_code == 201
    post_id = post.json["data"]["id"]

    res = client.post(
        f"/posts/{post_id}/like",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201
