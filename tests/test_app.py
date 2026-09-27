# tests/test_app.py
import os
os.environ["GAME_API_KEY"] = "dev-secret-key"
os.environ["FLASK_DEBUG"] = "false"

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pytest
from app import app

API_KEY = "dev-secret-key"
HEADERS = {"X-API-KEY": API_KEY}

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_get_state_returns_200(client):
    resp = client.get("/state")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "score1" in data
    assert "score2" in data

def test_authorized_move_succeeds(client):
    resp = client.post("/move", json={"player": 1, "direction": "up"}, headers=HEADERS)
    assert resp.status_code == 200

def test_unauthorized_reset_is_rejected(client):
    resp = client.post("/reset", json={})
    assert resp.status_code == 401

def test_unauthorized_move_is_rejected(client):
    resp = client.post("/move", json={"player": 1, "direction": "up"})
    assert resp.status_code == 401

def test_unauthorized_update_is_rejected(client):
    resp = client.post("/update", json={})
    assert resp.status_code == 401

def test_authorized_update_succeeds(client):
    resp = client.post("/update", json={}, headers=HEADERS)
    assert resp.status_code == 200

def test_invalid_move_payload_returns_400(client):
    resp = client.post("/move", json={"player": 9, "direction": "sideways"}, headers=HEADERS)
    assert resp.status_code == 400