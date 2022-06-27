from collections import deque
from assertpy import assert_that, soft_assertions
import pytest

from app.setgame import Game
from app.setgame import Card, Shape, Shading, Number, Color


@pytest.fixture
def standard_deck():
    cards = [
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.THREE, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.OVAL, shading=Shading.STRIPED, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.EMPTY, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.SOLID, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.ONE, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.ONE, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.EMPTY, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.SQUIGGLE, shading=Shading.STRIPED, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.EMPTY, number=Number.TWO, color=Color.BLUE),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.TWO, color=Color.RED),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.TWO, color=Color.GREEN),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.THREE, color=Color.RED),
        Card(shape=Shape.DIAMOND, shading=Shading.STRIPED, number=Number.THREE, color=Color.BLUE),
        Card(shape=Shape.OVAL, shading=Shading.SOLID, number=Number.ONE, color=Color.RED),
        Card(shape=Shape.SQUIGGLE, shading=Shading.SOLID, number=Number.ONE, color=Color.GREEN)
    ]
    return deque(cards) 


@pytest.fixture
def larger_deck():
    cards = [
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.RED, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.STRIPED, shape=Shape.OVAL, color=Color.GREEN, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.RED, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.STRIPED, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.OVAL, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.BLUE, number=Number.TWO), 
        Card(shading=Shading.EMPTY, shape=Shape.DIAMOND, color=Color.BLUE, number=Number.THREE), 
        Card(shading=Shading.SOLID, shape=Shape.DIAMOND, color=Color.GREEN, number=Number.TWO), 
        Card(shading=Shading.SOLID, shape=Shape.SQUIGGLE, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.OVAL, color=Color.GREEN, number=Number.ONE), 
        Card(shading=Shading.EMPTY, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.THREE), 
        Card(shading=Shading.STRIPED, shape=Shape.SQUIGGLE, color=Color.RED, number=Number.THREE)
    ]
    return deque(cards)

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
    game.add_player('jeff')
    game.add_player('ted')
    game.add_player('ron')

    with soft_assertions():
        assert_that(game.players).contains_key('jeff')
        assert_that(game.players).contains_key('ted')
        assert_that(game.players).contains_key('ron')


def test_it_cant_add_the_same_player_twice():
    game = Game()
    game.add_player('jeff')

    with pytest.raises(ValueError):
        game.add_player('jeff')