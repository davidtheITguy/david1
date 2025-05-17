"""Simple WebSocket server and client example.

This module provides two classes:
- `WebSocketServer`: launches an asynchronous WebSocket server
  that echos messages back to connected clients.
- `WebSocketClient`: connects to a WebSocket server and allows
  sending and receiving messages.

The code uses the `websockets` package which must be installed
(`pip install websockets`).
"""

import asyncio
import websockets


class WebSocketServer:
    """A basic WebSocket echo server."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self._server = None

    async def _handler(self, websocket, path):
        async for message in websocket:
            await websocket.send(message)

    async def start(self):
        self._server = await websockets.serve(self._handler, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        await self._server.wait_closed()

    def run(self):
        asyncio.run(self.start())


class WebSocketClient:
    """A simple WebSocket client."""

    def __init__(self, uri: str = "ws://localhost:8765"):
        self.uri = uri

    async def send_and_receive(self, message: str) -> str:
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            return response

    def run(self, message: str):
        return asyncio.run(self.send_and_receive(message))


if __name__ == "__main__":
    # Example usage when running this module directly.
    server = WebSocketServer()

    async def demo():
        server_task = asyncio.create_task(server.start())
        await asyncio.sleep(1)  # Give server time to start
        client = WebSocketClient()
        response = await client.send_and_receive("hello")
        print(f"Client received: {response}")
        server._server.close()
        await server._server.wait_closed()
        server_task.cancel()

    asyncio.run(demo())

