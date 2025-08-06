from flask import json, url_for
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token

app = create_app()

def test_user_registration(client):
    response = client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json['msg'] == 'User created'

def test_user_login(client):
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

def test_token_generation(client):
    client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post(url_for('auth.login'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    access_token = login_response.json['access_token']
    assert access_token is not None

def test_user_registration_duplicate(client):
    client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post(url_for('auth.register'), json={
        'username': 'testuser',
        'password': 'newpassword'
    })
    assert response.status_code == 400
    assert response.json['msg'] == 'User already exists'