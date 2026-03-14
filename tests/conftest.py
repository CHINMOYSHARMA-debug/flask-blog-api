import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app()
    
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
    
@pytest.fixture
def token(client):

    client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })

    res = client.post("/login", json={
        "username": "testuser",
        "password": "123456"
    })

    return res.json["data"]["access_token"]
