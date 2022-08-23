import typing

from starlette.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.connections: typing.List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await self.add_connection(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.connections.remove(websocket)

    async def add_connection(self, websocket: WebSocket) -> None:
        self.connections.append(websocket)

    async def send_message(self, websocket: WebSocket, message: dict) -> None:
        await websocket.send_json(message)

    async def broadcast(self, message: dict) -> None:
        for connection in self.connections:
            await connection.send_json(message)

    async def broadcast_exclude(self, websocket: typing.List[WebSocket], message: dict) -> None:
        for connection in self.connections:
            if connection not in websocket:
                await connection.send_json(message)
