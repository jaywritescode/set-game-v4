from marshmallow import Schema, fields
import marshmallow_dataclass

from app.setgame import Card


CardSchema = marshmallow_dataclass.class_schema(Card)()


GameSchema = Schema.from_dict({
    "board": fields.List(fields.Nested(CardSchema)),
    "players": fields.Dict(keys=fields.Str(), values=fields.List(fields.List(fields.Nested(CardSchema)))),
    "game_over": fields.Boolean()
})