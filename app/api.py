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


class GameApi(WebSocketEndpoint):
    def __init__(self, scope, receive, send):
        super().__init__(scope, receive=receive, send=send)

        if self.connections is None:
            self.scope['app'].state.connections = ConnectionManager()
        if self.game is None:
            self.scope['app'].state.game = Game()


    @property
    def connections(self):
        return getattr(self.scope['app'].state, 'connections', None)

    @property
    def game(self):
        return getattr(self.scope['app'].state, 'game', None)

    async def on_connect(self, websocket):
        await self.connections.accept(websocket)
        await websocket.send_text('Hello, world!')
        await websocket.close()

    async def on_receive(self, websocket, data):
        pass

    async def on_disconnect(self, websocket, close_code):
        await super().on_disconnect(websocket, close_code)
        self.connections.disconnect(websocket)


routes = [
    WebSocketRoute('/ws', GameApi)
]
app = Starlette(debug=True, routes=routes)