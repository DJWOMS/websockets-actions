import typing

from starlette.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.connections: typing.List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await self.add_connection(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def add_connection(self, websocket: WebSocket):
        self.connections.append(websocket)

    async def send_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.connections:
            await connection.send_json(message)
