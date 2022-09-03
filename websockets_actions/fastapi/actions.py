from starlette.websockets import WebSocket

from websockets_actions.broadcast.manager import WebSocketManager
from websockets_actions.fastapi.endpoints import WebSocketFastAPI
from websockets_actions.starlette.mixin import ActionsMixin


class WebSocketActions(ActionsMixin, WebSocketFastAPI):
    encoding = 'json'


class WebSocketBroadcast(WebSocketActions):
    manager = WebSocketManager()

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        await self.manager.connect(websocket)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await self.manager.disconnect(websocket)
