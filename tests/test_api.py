from assertpy import assert_that
from starlette.testclient import TestClient

from app.api import app


def test_app():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = websocket.receive_text()
        assert data == 'Hello, world!'


def test_first_player_connects():
    client = TestClient(app)
    with client.websocket_connect('/ws'):
        assert_that(app.state.connections).is_length(1)


def test_multiple_players_connect():
    client = TestClient(app)
    with client.websocket_connect('/ws'), client.websocket_connect('/ws'):
        assert_that(app.state.connections).is_length(2)


def test_player_joins_game():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        websocket.receive_text()
        websocket.send_json({'action': 'join_game', 'payload': {'name': 'tom'}})
        data = websocket.receive_json()
        assert_that(data).contains_entry({'tom': []})