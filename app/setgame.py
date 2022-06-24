from collections import deque
from dataclasses import dataclass, fields
from enum import Enum
from itertools import combinations, product
import random


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
    """Given cards c and d, find the unique card e such that (c, d, e) is a Set.
    """
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
        if len(self.board):
            return

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
            raise ValueError(f"{name} is already playing.")

        self.players[name] = list()

    def has_set(self):
        return contains_set(self.board)

    def is_started(self):
        return self.board

    def is_game_over(self):
        return self.game_over