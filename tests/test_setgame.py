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


def test_it_deals_twelve_cards(standard_deck):
    game = Game()
    game.cards = standard_deck

    with soft_assertions():
        assert_that(game.deal()).is_true()
        assert_that(game.board).is_length(12)
        assert_that(game.cards).is_length(69)