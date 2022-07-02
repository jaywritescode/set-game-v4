from operator import itemgetter
from marshmallow import Schema, fields
from marshmallow_dataclass import dataclass
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute

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
        "action": fields.Str(),
        "payload": fields.Dict(keys=fields.Str(), values=fields.Str()),
    }
)

JoinGameRequestSchema = Schema.from_dict(
    {
        "name": fields.Str()
    }
)


class GameApi(WebSocketEndpoint):
    encoding = "json"

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
        await websocket.send_text("Hello, world!")

    async def on_receive(self, websocket, data):
        schema = MessageSchema()
        message = schema.dump(data)

        action = message["action"]
        try:        
        if action == "join_game":
                result = self.handle_join_game(JoinGameRequestSchema().dump(message['payload']))

    async def on_disconnect(self, websocket, close_code):
        await super().on_disconnect(websocket, close_code)
        self.connections.disconnect(websocket)

    def handle_join_game(self, request):
            try:
            self.game.add_player(request['name'])
            # TODO: really you want to return the entire game
                return self.game.players
        except ValueError as e:
            raise e

        return None


routes = [WebSocketRoute("/ws", GameApi)]
app = Starlette(debug=True, routes=routes)
