from collections import deque
from assertpy import assert_that, soft_assertions
import pytest

from app.setgame import Game
from app.setgame import Card, Shape, Shading, Number, Color


################################################
# test that it deals the correct number of cards
################################################
def test_it_deals_twelve_cards(standard_deck):
    game = Game()
    game.cards = standard_deck

    with soft_assertions():
        assert_that(game.deal()).is_true()
        assert_that(game.board).is_length(12)
        assert_that(game.cards).is_length(69)


def test_it_deals_eighteen_cards(larger_deck):
    game = Game()
    game.cards = larger_deck

    with soft_assertions():
        assert_that(game.deal()).is_true()
        assert_that(game.board).is_length(18)
        assert_that(game.cards).is_length(63)


################################################
# test that it adds players
################################################
def test_it_adds_players():
    game = Game()
    game.add_player("jeff")
    game.add_player("ted")
    game.add_player("ron")

    with soft_assertions():
        assert_that(game.players).contains_key("jeff")
        assert_that(game.players).contains_key("ted")
        assert_that(game.players).contains_key("ron")


def test_it_cant_add_the_same_player_twice():
    game = Game()
    game.add_player("jeff")

    with pytest.raises(RuntimeError):
        game.add_player("jeff")


################################################
# test that a player can find a Set
################################################
def test_handle_player_finds_valid_set(standard_deck):
    game = Game()
    game.cards = standard_deck
    game.add_player("jeff")
    game.deal()

    cards = [
        Card(
            shape=Shape.OVAL,
            shading=Shading.SOLID,
            number=Number.THREE,
            color=Color.GREEN,
        ),
        Card(
            shape=Shape.SQUIGGLE,
            shading=Shading.EMPTY,
            number=Number.ONE,
            color=Color.RED,
        ),
        Card(
            shape=Shape.DIAMOND,
            shading=Shading.STRIPED,
            number=Number.TWO,
            color=Color.BLUE,
        ),
    ]

    with soft_assertions():
        assert_that(game.handle_player_finds_set(cards, player="jeff")).is_true()
        assert_that(game.players["jeff"]).is_length(1)
        assert_that(game.board).is_length(12)
        assert_that(game.cards).is_length(66)


def test_handle_player_finds_set_not_on_board(standard_deck):
    game = Game()
    game.cards = standard_deck
    game.add_player("jeff")
    game.deal()

    cards = [
        Card(
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            number=Number.ONE,
            color=Color.RED,
        ),
        Card(
            shape=Shape.SQUIGGLE,
            shading=Shading.EMPTY,
            number=Number.ONE,
            color=Color.GREEN,
        ),
        Card(
            shape=Shape.SQUIGGLE,
            shading=Shading.STRIPED,
            number=Number.ONE,
            color=Color.BLUE,
        ),
    ]

    with soft_assertions():
        with pytest.raises(RuntimeError):
            game.handle_player_finds_set(cards, player="jeff")
        assert_that(game.players["jeff"]).is_length(0)
        assert_that(game.board).is_length(12)
        assert_that(game.cards).is_length(69)


def test_handle_player_finds_invalid_set(standard_deck):
    game = Game()
    game.cards = standard_deck
    game.add_player("jeff")
    game.deal()

    cards = [
        Card(
            shape=Shape.DIAMOND,
            shading=Shading.SOLID,
            number=Number.TWO,
            color=Color.GREEN,
        ),
        Card(
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            number=Number.TWO,
            color=Color.GREEN,
        ),
        Card(
            shape=Shape.SQUIGGLE,
            shading=Shading.SOLID,
            number=Number.ONE,
            color=Color.RED,
        ),
    ]

    with soft_assertions():
        assert_that(game.handle_player_finds_set(cards, player="jeff")).is_false()
        assert_that(game.players["jeff"]).is_length(0)
        assert_that(game.board).is_length(12)
        assert_that(game.cards).is_length(69)
