import asyncio

from autobahn.asyncio.websocket import WebSocketServerProtocol

loop = asyncio.get_event_loop()


class WSServerProtocol(WebSocketServerProtocol):
    """
    Websocket server protocol.
    """
    CLIENTS = set()

    def onConnect(self, request):
        self.CLIENTS.add(self)

    def onMessage(self, payload, is_binary):
        for client in self.CLIENTS:
            # send this message to all clients
            if client is not self:
                try:
                    client.sendMessage(payload, is_binary)
                except Exception as e:
                    print(e)

    def onClose(self, was_clean, code, reason):
        self.CLIENTS.remove(self)

        if not self.CLIENTS:
            loop.stop()

    # comes from >>> class WebSocketAdapterProtocol(asyncio.Protocol):...
    def connection_made(self, transport):
        super(WSServerProtocol, self).connection_made(transport)

    def connection_lost(self, exc):
        super(WSServerProtocol, self).connection_lost(exc)
