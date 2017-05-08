import json

from autobahn.asyncio.websocket import WebSocketClientProtocol

from config import DEBUG, CLIENTS_MSGS_COUNT, CLIENTS_COUNT


class WSClientProtocol(WebSocketClientProtocol):
    """
    Websocket client protocol.
    """

    def __init__(self):
        super(WSClientProtocol, self).__init__()
        self._msgs_received = 0
        self._disconect_after = CLIENTS_COUNT * CLIENTS_MSGS_COUNT - CLIENTS_MSGS_COUNT

    def _print(self, msg):
        if DEBUG:
            print('Client {}: {}'.format(id(self), msg))

    def onConnect(self, response):
        self._print('connected: {}.'.format(response.peer))

    def onOpen(self):
        self._print('ws connection opened.')

        msg_bin = json.dumps(
            {
                'client_id': id(self),
                'message': 'Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a.'
            }
        ).encode('utf8')

        for _ in range(CLIENTS_MSGS_COUNT):
            self.sendMessage(msg_bin, isBinary=True)

    def onMessage(self, payload, is_binary):
        if is_binary:
            self._print('binary msg {} received: {} bytes'.format(self._msgs_received, len(payload)))
            self._msgs_received += 1

        if self._msgs_received == self._disconect_after:
            self._print('sendClose')
            self.sendClose(code=1000, reason='we_are_tired')

    def onClose(self, wasClean, code, reason):
        self._print('connection closed: {}.'.format(reason))
