from collections import deque
from dataclasses import fields
from enum import Enum
from itertools import combinations, product
import random
import marshmallow as mm
from marshmallow_dataclass import dataclass


Number = Enum("Number", "ONE TWO THREE", start=0)

Color = Enum("Color", "RED BLUE GREEN", start=0)

Shading = Enum("Shading", "EMPTY SOLID STRIPED", start=0)

Shape = Enum("Shape", "DIAMOND OVAL SQUIGGLE", start=0)


@dataclass(frozen=True)
class Card:
    number: Number
    color: Color
    shading: Shading
    shape: Shape

    def index(self):
        return sum(
            getattr(self, field.name).value * (3**i)
            for (i, field) in enumerate(fields(Card))
        )


def is_set(cards):
    """Given some collection of cards, determine if they form a Set.

    :param cards: a collection of cards
    :return: True if the cards form a Set, otherwise False.
    """
    if len(cards) != 3:
        return False

    for field in fields(Card):
        if not sum(getattr(card, field.name).value for card in cards) % 3 == 0:
            return False
    return True


def complete_set(c, d):
    """Given cards c and d, find the unique card e such that (c, d, e) is a Set."""
    number = Number(-(c.number.value + d.number.value) % 3)
    color = Color(-(c.color.value + d.color.value) % 3)
    shading = Shading(-(c.shading.value + d.shading.value) % 3)
    shape = Shape(-(c.shape.value + d.shape.value) % 3)
    return Card(number, color, shading, shape)


def contains_set(cards):
    """Given a collection of cards, determine if any three of them form a Set.

    :param cards: a collection of cards
    :return: True if any three cards in the collection form a Set, otherwise False
    """
    if len(cards) < 3:
        return False

    return any(complete_set(*pair) in cards for pair in combinations(cards, 2))


def deck():
    return [Card(*attrs) for attrs in product(Number, Color, Shading, Shape)]


class Game:
    def __init__(self):
        self.cards = deque(deck())
        self.board = []
        self.players = dict()
        self.game_over = False

    def start(self):
        if len(self.board) or self.game_over:
            raise RuntimeError("game is already started")

        self.shuffle()
        self.deal()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        """Deal cards to the board.

        :return: True if there are at least twelve cards on the board and at least one Set.
        """
        while len(self.board) < 12 or not self.has_set():
            if not self.cards:
                # no more cards in the deck
                return False

            for _ in range(3):
                self.board.append(self.cards.popleft())

        return True

    def add_player(self, name):
        if name in self.players:
            raise RuntimeError(f"{name} is already playing.")

        self.players[name] = list()

    def handle_player_finds_set(self, cards, *, player):
        """Given a player's selection of cards, validate that the selection makes a Set and, if valid, give that Set to the player.

        :param cards: a collection of cards
        :param player: the player
        :return: True iff the cards (and player) are valid
        """
        if not (
            self.player_exists(player)
            and all(self.card_is_on_board(card) for card in cards)
            and is_set(cards)
        ):
            return False

        self.board = [card for card in self.board if card not in cards]
        self.players[player].append(cards)

        self.deal()
        return True

    def has_set(self):
        return contains_set(self.board)

    def card_is_on_board(self, card):
        return card in self.board

    def player_exists(self, player):
        return player in self.players

    def is_started(self):
        return self.board

    def is_game_over(self):
        return self.game_over


class GameSchema(mm.Schema):
    board = mm.fields.List(mm.fields.Nested(Card.Schema()))
    players = mm.fields.Dict(keys=mm.fields.Str(), values=mm.fields.List(mm.fields.List(mm.fields.Nested(Card.Schema()))))
    game_over = mm.fields.Boolean()