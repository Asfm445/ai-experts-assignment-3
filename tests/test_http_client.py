import time

import requests

from app.http_client import Client
from app.tokens import OAuth2Token, token_from_iso


def test_client_uses_requests_session():
    c = Client()
    c.oauth2_token = OAuth2Token(access_token="ok", expires_at=int(time.time()) + 3600)
    resp = c.request("GET", "/me", api=True)
    assert isinstance(c.session, requests.Session)
    assert resp["headers"].get("Authorization") == "Bearer ok"
    assert resp["method"] == "GET"
    assert resp["path"] == "/me"



def test_token_from_iso_uses_dateutil():
    token = token_from_iso("ok", "2099-01-01T00:00:00Z")
    assert isinstance(token, OAuth2Token)
    assert token.access_token == "ok"
    assert not token.expired

    c = Client()
    c.oauth2_token = token
    resp = c.request("GET", "/me", api=True)
    assert resp["headers"].get("Authorization") == "Bearer ok"
    assert resp["method"] == "GET"
    assert resp["path"] == "/me"



def test_api_request_sets_auth_header_when_token_is_valid():
    c = Client()
    c.oauth2_token = OAuth2Token(access_token="ok", expires_at=int(time.time()) + 3600)

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer ok"
    assert resp["method"] == "GET"
    assert resp["path"] == "/me"


def test_api_request_refreshes_when_token_is_missing():
    c = Client()
    c.oauth2_token = None

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"


def test_api_request_refreshes_when_token_is_dict():
    c = Client()
    c.oauth2_token = {"access_token": "stale", "expires_at": 0}

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer fresh-token"
    


def test_api_request_success_when_token_is_dict_and_valid():
    c = Client()
    c.oauth2_token = {"access_token": "ok", "expires_at": int(time.time()) + 3600}

    resp = c.request("GET", "/me", api=True)
    assert resp["headers"].get("Authorization") == "Bearer ok"
    assert resp["method"] == "GET"
    assert resp["path"] == "/me"


def test_iso_dict_token_sets_auth_header():
    c = Client()
    c.oauth2_token = {
        "access_token": "ok",
        "expires_at": "2099-01-01T00:00:00Z"
    }

    resp = c.request("GET", "/me", api=True)

    assert resp["headers"].get("Authorization") == "Bearer ok"
    assert resp["method"] == "GET"
    assert resp["path"] == "/me"
