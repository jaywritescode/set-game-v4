from marshmallow import Schema, ValidationError, fields
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from app.serialize import CardSchema, GameSchema

from app.setgame import Game


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def accept(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)

    def __len__(self):
        return len(self.active_connections)


MessageSchema = Schema.from_dict(
    {
        "action": fields.Str(),  # TODO: validate that this only takes on "join_game", "start_game", "submit"
        "payload": fields.Dict(keys=fields.Str()),
    }
)

JoinGameRequestSchema = Schema.from_dict({"name": fields.Str(required=True)})


SubmitRequestSchema = Schema.from_dict(
    {"player": fields.Str(), "cards": fields.List(fields.Nested(CardSchema))}
)


ResponseSchema = Schema.from_dict(
    {
        "success": fields.Boolean(),
        "game": fields.Nested(GameSchema),
        "error": fields.Str(),
    }
)


class GameApi(WebSocketEndpoint):
    encoding = "json"

    game_schema = GameSchema()

    def __init__(self, scope, receive, send):
        super().__init__(scope, receive=receive, send=send)

        if self.connections is None:
            self.scope["app"].state.connections = ConnectionManager()
        if self.game is None:
            self.scope["app"].state.game = Game()

    @property
    def connections(self):
        return getattr(self.scope["app"].state, "connections", None)

    @property
    def game(self):
        return getattr(self.scope["app"].state, "game", None)

    async def on_connect(self, websocket):
        await self.connections.accept(websocket)

    async def on_receive(self, websocket, data):
        schema = MessageSchema()
        message = schema.dump(data)

        action = message["action"]

        try:
            if action == "join_game":
                result = self.handle_join_game(
                    JoinGameRequestSchema().load(message["payload"])
                )
            elif action == "start_game":
                result = self.handle_start_game()
            elif action == "submit":
                result = self.handle_submit(
                    SubmitRequestSchema().load(message["payload"])
                )
        except ValidationError as e:
            result = ResponseSchema().dump({"success": False, "error": e})

        result = schema.load({"action": action, "payload": result})
        await self.connections.broadcast(result)

    async def on_disconnect(self, websocket, close_code):
        await super().on_disconnect(websocket, close_code)
        self.connections.disconnect(websocket)

    #############################################
    # join game
    #############################################
    def handle_join_game(self, request):
        """Handles a request to join the game.

        :param request: the request
        :returns json: an outgoing message with the result
        """
        # TODO: don't assume that two players won't have the same name
        self.add_player(request["name"])
        return ResponseSchema().dump({"success": True, "game": self.game})

    def add_player(self, name):
        self.game.add_player(name)

    #############################################
    # start game
    #############################################
    def handle_start_game(self):
        try:
            self.game.start()
            return ResponseSchema().dump({"success": True, "game": self.game})
        except RuntimeError as e:
            return ResponseSchema().dump({"success": False, "error": e})

    #############################################
    # submit
    #############################################
    def handle_submit(self, request):
        player = request["player"]
        cards = request["cards"]

        try:
            if not self.game.player_exists(player):
                raise RuntimeError(f"player {player} has not joined game")

            if self.submit(cards, player):
                return ResponseSchema().dump({"success": True, "game": self.game})
            else:
                return ResponseSchema().dump(
                    {
                        "success": False,
                        "game": self.game,
                        "error": f"Not a set: {cards}",
                    }
                )
        except RuntimeError as e:
            return ResponseSchema().dump({"success": False, "error": e})

    def submit(self, cards, player):
        return self.game.handle_player_finds_set(cards, player=player)


routes = [WebSocketRoute("/ws", GameApi)]
app = Starlette(debug=True, routes=routes)
