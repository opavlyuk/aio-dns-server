import asyncio

from aio_dns_server.resolvers import PyHoleResolver
from aio_dns_server.server import DNSServer, DNSDatagramProtocol


async def launcher():
    upstream_dns = '193.41.60.1'
    resolver = PyHoleResolver(upstream_dns)
    server = DNSServer(resolver, protocol=DNSDatagramProtocol)
    await server.start()
    await asyncio.sleep(3600)  # Serve for 1 hour.


def main():
    asyncio.run(launcher())
