# Чат на Starlette

# Зависимости

    pip websockets-actions
    pip install jinja2

# Структура проекта

    src:
        - endpoints.py
        - routes.py
    static:
        - scripts.js
        - style.css
    templates:
        - index.html
    main.py

# Использование

### Файл main.py

    from starlette.applications import Starlette

    from src import routes
    
    app = Starlette(
        debug=True, 
        routes=routes
    )

Файл routes.py мы создадим позже.

### Файл templates/index.html

    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <link rel="stylesheet" href="/static/style.css">
      <title>Chat</title>
    </head>
    <body>
    <h1>WebSocket Chat</h1>
    
    <form id="form-username">
      <input type="text" id="username" autocomplete="off" placeholder="Your name"/>
      <button type="button" id="create-name">Open chat</button>
    </form>
    
    <div id="form-chat">
      <h5>Chat</h5>
    
      <ul id='messages'>
      </ul>
    
      <form>
        <input type="text" id="messageText" autocomplete="off" placeholder="Your message"/>
        <button type="button" id="send-message">Send</button>
      </form>
    
      <p><button type="button" id="close-chat">Close</button></p>
    </div>
    
    <script src="/static/scripts.js"></script>
    </body>
    </html>

### Файл static/style.css

    #form-chat {
        display: none;
    }

### Файл static/scripts.js

    const messages = document.getElementById('messages')
    document.getElementById('send-message').addEventListener('click', sendMessage)
    document.getElementById('create-name').addEventListener('click', createUsername)
    document.getElementById('close-chat').addEventListener('click', closeChat)
    
    let username
    
    const ws = new WebSocket("ws://localhost:8000/ws")
    
    
    ws.onmessage = function (event) {
        let data = JSON.parse(event.data)
        switch (data.action) {
            case 'join':
                joinUser(data.message)
                break
            case 'newMessage':
                newMessage(data.username, data.message)
                break
            case 'disconnect':
                disconnectUser(data.message)
                break
            default:
                break
        }
    }
    
    function joinUser(message) {
        let li = document.createElement('li')
        let content = document.createTextNode(`Connected user: ${message}`)
        li.appendChild(content)
        messages.appendChild(li)
    }
    
    function newMessage(username, message) {
        let li = document.createElement('li')
        let content = document.createTextNode(`${username}: ${message}`)
        li.appendChild(content)
        messages.appendChild(li)
    }
    
    function disconnectUser(message) {
        let li = document.createElement('li')
        let content = document.createTextNode(`Disconnected user: ${message}`)
        li.appendChild(content)
        messages.appendChild(li)
    }
    
    function sendMessage(event) {
        let input = document.getElementById("messageText")
        let data = JSON.stringify(
            {
                action: 'send_message',
                username: username,
                message: input.value
            }
        )
        ws.send(data)
        input.value = ''
    }
    
    function createUsername() {
        username = document.getElementById("username").value
        let formUsername = document.getElementById("form-username")
        formUsername.style.display = 'none'
    
        let formChat = document.getElementById("form-chat")
        formChat.style.display = 'block'
    
        let data = JSON.stringify(
            {
                action: 'join',
                username: username
            }
        )
        ws.send(data)
    }
    
    function closeChat() {
        let data = JSON.stringify(
            {
                action: 'close',
                username: username
            }
        )
        ws.send(data)
    
        document.getElementById("username").value = ''
        let formUsername = document.getElementById("form-username")
        formUsername.style.display = 'block'
    
        let formChat = document.getElementById("form-chat")
        formChat.style.display = 'none'
    }

### Файл endpoints.py

    from typing import Any, List

    from starlette.endpoints import HTTPEndpoint
    from starlette.requests import Request
    from starlette.templating import Jinja2Templates
    from starlette.websockets import WebSocket
    
    from websockets_actions.actions import WebSocketBroadcast
    
    
    class HomePage(HTTPEndpoint):
        async def get(self, request: Request) -> Jinja2Templates.TemplateResponse:
            template = Jinja2Templates(directory='templates')
            return template.TemplateResponse('index.html', {'request': request})
    
    
    class ChatWebSockets(WebSocketBroadcast):
        actions: List[str] = ['join', 'send_message', 'close']
    
        async def join(self, websocket: WebSocket, data: Any) -> None:
            await self.manager.broadcast({'action': 'join', 'message': data.get('username')})
    
        async def send_message(self, websocket: WebSocket, data: Any) -> None:
            await self.manager.broadcast({
                'action': 'newMessage',
                'username': data.get('username'),
                'message': data.get('message')
            })
    
        async def close(self, websocket: WebSocket, data: Any | None = None) -> None:
            await super().on_disconnect(websocket, 1000)
            await self.manager.broadcast_exclude(
                [websocket],
                {'action': 'disconnect', 'message': data.get('username')}
            )

### Файл routs.py

    from starlette.routing import Route, Mount, WebSocketRoute
    from starlette.staticfiles import StaticFiles
    
    from .endpoints import HomePage, ChatWebSockets
    
    routes = [
        Route('/', HomePage),
        WebSocketRoute('/ws', ChatWebSockets),
        Mount('/static', app=StaticFiles(directory='static'))
    ]


[Полный пример](https://github.com/DJWOMS/chat_websockets_actions_starlette)
