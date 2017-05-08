import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from datetime import datetime

from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketClientFactory

from protocols import WSServerProtocol, WSClientProtocol
from config import HOST, PORT, CLIENTS_COUNT


start = datetime.now()

# our uvloop loop
loop = asyncio.get_event_loop()

# server factory
server_factory = WebSocketServerFactory("ws://{}:{}".format(HOST, PORT))
server_factory.protocol = WSServerProtocol

_generator = loop.create_server(server_factory, port=PORT)
# we are going to connect our clients only after server was created
ws_server = loop.run_until_complete(_generator)

# let's create clients
client_factory = WebSocketClientFactory("ws://{}:{}".format(HOST, PORT))
client_factory.protocol = WSClientProtocol

tasks = []
for _ in range(CLIENTS_COUNT):
    tasks.append(loop.create_connection(client_factory, HOST, PORT))
loop.run_until_complete(asyncio.gather(*tasks))

loop.run_forever()

# get/print alpha seconds
alpha = datetime.now() - start
print('Seconds {}'.format(alpha.total_seconds()))

loop.close()
