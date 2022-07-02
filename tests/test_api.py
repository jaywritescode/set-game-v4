from assertpy import assert_that
from starlette.testclient import TestClient

from app.api import app


def test_app():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, world!"


def test_first_player_connects():
    client = TestClient(app)
    with client.websocket_connect("/ws"):
        assert_that(app.state.connections).is_length(1)


def test_multiple_players_connect():
    client = TestClient(app)
    with client.websocket_connect("/ws"), client.websocket_connect("/ws"):
        assert_that(app.state.connections).is_length(2)


def test_player_joins_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_text()
        websocket.send_json({"action": "join_game", "payload": {"name": "tom"}})
        data = websocket.receive_json()
        assert_that(data).contains_entry({"tom": []})


def test_invalid_join_game_request():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_text()
        websocket.send_json({"action": "join_game", "payload": {}})
        data = websocket.receive_json()
        assert_that(data).contains_key("error")


def test_multiple_players_join_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text(); ws2.receive_text()

        ws1.send_json({"action": "join_game", "payload": {"name": "tom"}})
        ws1.receive_json(); ws2.receive_json()

        ws2.send_json({"action": "join_game", "payload": {"name": "jim"}})
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()

        assert_that(data1).contains_entry({"tom": []}, {"jim": []})
        assert_that(data2).contains_entry({"tom": []}, {"jim": []})


def test_same_player_joins_game_multiple_times():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text(); ws2.receive_text()

        ws1.send_json({"action": "join_game", "payload": {"name": "tom"}})
        ws1.receive_json(); ws2.receive_json()

        ws2.send_json({"action": "join_game", "payload": {"name": "tom"}})
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()

        assert_that(data1).contains_key("error")
        assert_that(data2).contains_key("error")


def test_start_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text(); ws2.receive_text()

        ws1.send_json({"action": "join_game", "payload": {"name": "tim"}})
        ws1.receive_json(); ws2.receive_json()

        ws2.send_json({"action": "join_game", "payload": {"name": "joe"}})
        ws1.receive_json(); ws2.receive_json()

        ws1.send_json({"action": "start_game", "payload": {}})
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()
    
        assert_that(data1['game_over']).is_false
        assert_that(data1['board']).is_length(12)
        assert_that(data1['players']).contains_entry({"tim": []}, {"joe": []})

        assert_that(data2['game_over']).is_false
        assert_that(data2['board']).is_length(12)
        assert_that(data2['players']).contains_entry({"tim": []}, {"joe": []})


def test_multiple_calls_to_start_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_text()
        
        websocket.send_json({"action": "start_game", "payload": {}})
        websocket.receive_json()

        websocket.send_json({"action": "start_game", "payload": {}})
        data = websocket.receive_json()
        assert_that(data).contains_key("error")