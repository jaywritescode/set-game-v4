from assertpy import assert_that
from starlette.testclient import TestClient

from app.api import app


def test_app():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = websocket.receive_text()
        assert data == 'Hello, world!'


def test_first_player_joins_game():
    client = TestClient(app)
    with client.websocket_connect('/ws') as ws1:
        assert_that(app.state.connections).is_length(1)


def test_multiple_players_join_game():
    client = TestClient(app)
    with client.websocket_connect('/ws') as ws1, client.websocket_connect('/ws') as ws2:
        assert_that(app.state.connections).is_length(2)