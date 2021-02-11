import asyncio

from aio_dns_server.block_list import BlockList
from aio_dns_server.resolvers import PyHoleResolver
from aio_dns_server.server import DNSServer, DNSDatagramProtocol
from aio_dns_server.util.config_mgr import config


async def launcher():
    upstream_dns = config['main']['upstream_dns_addr']
    upstream_port = config['main']['upstream_dns_port']
    block_list = BlockList(config['main']['block_list'])
    resolver = PyHoleResolver(upstream_dns, upstream_port, block_list=block_list)
    server = DNSServer(address=config['main']['address'], port=config['main']['port'],
                       resolver=resolver, protocol=DNSDatagramProtocol)
    await server.start()
    return server


def main():
    try:
        loop = asyncio.get_event_loop()
        server = loop.run_until_complete(launcher())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.stop()
