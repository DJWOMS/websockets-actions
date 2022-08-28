import typing

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from .manager import WebSocketManager


class WebSocketActions(WebSocketEndpoint):
    encoding = 'json'
    actions: typing.List[str] = []

    async def actions_not_allowed(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({'action': 'Not found'})

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        if data['action'] in self.actions:
            handler = getattr(self, data['action'], self.actions_not_allowed)
        else:
            handler = self.actions_not_allowed
        return await handler(websocket, data)


class WebSocketBroadcast(WebSocketActions):
    manager = WebSocketManager()

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        await self.manager.connect(websocket)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await self.manager.disconnect(websocket)
