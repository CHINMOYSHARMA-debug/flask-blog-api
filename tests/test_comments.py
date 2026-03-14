def test_create_comment(client, token):

    post = client.post(   #create a post first
        "/posts",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test", "content": "Hello"} 
    )

    assert post.status_code == 201
    post_id = post.json["data"]["id"]

    res = client.post(   
        f"/posts/{post_id}/comments",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "text": "Nice post"
        }
    )

    assert res.status_code == 201