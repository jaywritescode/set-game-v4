from assertpy import assert_that
import pytest
from starlette.testclient import TestClient

from app.api import app


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

        expected = {
            "action": "join_game",
            "payload": {
                "success": True,
                "game": {
                    "players": {
                        "tom": [],
                    },
                    "board": [],
                    "game_over": False,
                },
            },
        }
        assert_that(data).is_equal_to(expected)


def test_multiple_players_join_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text()
        ws2.receive_text()

        ws1.send_json({"action": "join_game", "payload": {"name": "tom"}})
        ws1.receive_json()
        ws2.receive_json()

        ws2.send_json({"action": "join_game", "payload": {"name": "jim"}})
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()

        expected = {
            "action": "join_game",
            "payload": {
                "success": True,
                "game": {
                    "players": {"tom": [], "jim": []},
                    "board": [],
                    "game_over": False,
                },
            },
        }
        assert_that(data1).is_equal_to(expected)
        assert_that(data2).is_equal_to(expected)


def test_invalid_join_game_request():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_text()
        websocket.send_json({"action": "join_game", "payload": {}})
        data = websocket.receive_json()

        assert_that(data["action"]).is_equal_to("join_game")
        assert_that(data["payload"]).has_success(False)
        assert_that(data["payload"]).contains_key("error")


@pytest.mark.skip
def test_same_player_joins_game_multiple_times():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text()
        ws2.receive_text()

        ws1.send_json({"action": "join_game", "payload": {"name": "tom"}})
        ws1.receive_json()
        ws2.receive_json()

        ws2.send_json({"action": "join_game", "payload": {"name": "tom"}})
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()

        expected = {
            "action": "join_game",
            "payload": {"success": False, "error": "tom is already playing."},
        }
        assert_that(data1).is_equal_to(expected)
        assert_that(data2).is_equal_to(expected)


def test_start_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text()
        ws2.receive_text()

        app.state.game.add_player("tim")
        app.state.game.add_player("joe")

        ws1.send_json({"action": "start_game", "payload": {}})
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()

        assert_that(data1).is_equal_to(data2)

        assert_that(data1).has_action("start_game")
        assert_that(data1["payload"]["success"]).is_true()
        assert_that(data1["payload"]["game"]["board"]).is_length(12)
        assert_that(data1["payload"]["game"]["players"]).contains_entry(
            {"tim": []}, {"joe": []}
        )


def test_multiple_calls_to_start_game():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_text()

        websocket.send_json({"action": "start_game", "payload": {}})
        websocket.receive_json()

        websocket.send_json({"action": "start_game", "payload": {}})
        data = websocket.receive_json()

        assert_that(data).has_action("start_game")
        assert_that(data["payload"]).has_success(False)
        assert_that(data["payload"]).contains_key("error")


def test_player_submits_valid_set(standard_deck):
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws1, client.websocket_connect("/ws") as ws2:
        ws1.receive_text()
        ws2.receive_text()

        app.state.game.add_player("dan")
        app.state.game.add_player("lou")

        app.state.game.cards = standard_deck
        app.state.game.deal()

        ws1.send_json(
            {
                "action": "submit",
                "payload": {
                    "player": "lou",
                    "cards": [
                        {
                            "shape": "OVAL",
                            "shading": "SOLID",
                            "number": "THREE",
                            "color": "GREEN",
                        },
                        {
                            "shape": "SQUIGGLE",
                            "shading": "EMPTY",
                            "number": "ONE",
                            "color": "RED",
                        },
                        {
                            "shape": "DIAMOND",
                            "shading": "STRIPED",
                            "number": "TWO",
                            "color": "BLUE",
                        },
                    ],
                },
            }
        )
        data1 = ws1.receive_json()
        data2 = ws2.receive_json()

        expected = {
            "action": "submit",
            "payload": {
                "success": True,
                "game": {
                    "players": {
                        "dan": [],
                        "lou": [
                            [
                                {
                                    "shape": "OVAL",
                                    "shading": "SOLID",
                                    "color": "GREEN",
                                    "number": "THREE",
                                },
                                {
                                    "shape": "SQUIGGLE",
                                    "shading": "EMPTY",
                                    "color": "RED",
                                    "number": "ONE",
                                },
                                {
                                    "shape": "DIAMOND",
                                    "shading": "STRIPED",
                                    "color": "BLUE",
                                    "number": "TWO",
                                },
                            ]
                        ],
                    },
                    "game_over": False,
                    "board": [
                        {
                            "shape": "OVAL",
                            "shading": "EMPTY",
                            "color": "RED",
                            "number": "THREE",
                        },
                        {
                            "shape": "DIAMOND",
                            "shading": "SOLID",
                            "color": "GREEN",
                            "number": "TWO",
                        },
                        {
                            "shape": "SQUIGGLE",
                            "shading": "SOLID",
                            "color": "GREEN",
                            "number": "TWO",
                        },
                        {
                            "shape": "SQUIGGLE",
                            "shading": "SOLID",
                            "color": "RED",
                            "number": "ONE",
                        },
                        {
                            "shape": "SQUIGGLE",
                            "shading": "EMPTY",
                            "color": "GREEN",
                            "number": "ONE",
                        },
                        {
                            "shape": "OVAL",
                            "shading": "EMPTY",
                            "color": "GREEN",
                            "number": "TWO",
                        },
                        {
                            "shape": "DIAMOND",
                            "shading": "SOLID",
                            "color": "BLUE",
                            "number": "ONE",
                        },
                        {
                            "shape": "OVAL",
                            "shading": "SOLID",
                            "color": "RED",
                            "number": "THREE",
                        },
                        {
                            "shape": "DIAMOND",
                            "shading": "SOLID",
                            "color": "RED",
                            "number": "ONE",
                        },
                        {
                            "shape": "SQUIGGLE",
                            "shading": "EMPTY",
                            "color": "BLUE",
                            "number": "ONE",
                        },
                        {
                            "shape": "SQUIGGLE",
                            "shading": "STRIPED",
                            "color": "GREEN",
                            "number": "TWO",
                        },
                        {
                            "shape": "DIAMOND",
                            "shading": "STRIPED",
                            "color": "GREEN",
                            "number": "TWO",
                        },
                    ],
                },
            },
        }

        assert_that(data1).is_equal_to(expected)
        assert_that(data2).is_equal_to(expected)


def test_player_submits_not_a_set(standard_deck):
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.receive_text()

        app.state.game.add_player("fred")

        app.state.game.cards = standard_deck
        app.state.game.deal()

        websocket.send_json(
            {
                "action": "submit",
                "payload": {
                    "player": "fred",
                    "cards": [
                        {
                            "shape": "OVAL",
                            "shading": "SOLID",
                            "number": "THREE",
                            "color": "GREEN",
                        },
                        {
                            "shape": "OVAL",
                            "shading": "EMPTY",
                            "number": "THREE",
                            "color": "RED",
                        },
                        {
                            "shape": "DIAMOND",
                            "shading": "STRIPED",
                            "number": "TWO",
                            "color": "BLUE",
                        },
                    ],
                },
            }
        )
        data = websocket.receive_json()

        assert_that(data['payload']['success']).is_false()
        assert_that(data['payload']).contains_key('error')
        assert_that(data['payload']).contains_key('game')
