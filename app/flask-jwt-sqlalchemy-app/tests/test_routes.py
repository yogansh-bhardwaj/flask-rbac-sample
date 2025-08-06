from flask import json, url_for
from app import create_app, db
from app.models import User

app = create_app()

def test_register(client):
    response = client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json

def test_login(client):
    client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post(url_for('auth.login'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_protected_route(client):
    response = client.post(url_for('auth.login'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    access_token = response.json['access_token']
    response = client.get(url_for('some_protected_route'), headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200

def test_invalid_login(client):
    response = client.post(url_for('auth.login'), json={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_register_existing_user(client):
    client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 400
    assert 'message' in response.json
