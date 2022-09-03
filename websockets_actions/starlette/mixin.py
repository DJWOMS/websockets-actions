import typing

from starlette.websockets import WebSocket


class ActionsMixin:
    actions: typing.List[str] = []

    async def actions_not_allowed(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({'action': 'Not found'})

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        if data['action'] in self.actions:
            handler = getattr(self, data['action'], self.actions_not_allowed)
        else:
            handler = self.actions_not_allowed
        return await handler(websocket, data)
