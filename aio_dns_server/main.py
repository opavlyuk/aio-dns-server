import asyncio
import multiprocessing

from aio_dns_server.resolvers import PyHoleResolver
from aio_dns_server.server import DNSServer, DNSDatagramProtocol


async def launcher():
    upstream_dns = '193.41.60.1'
    resolver = PyHoleResolver(upstream_dns)
    server = DNSServer(resolver, protocol=DNSDatagramProtocol)
    await server.start()
    await asyncio.sleep(3600)  # Serve for 1 hour.


def main():
    # asyncio.run(launcher())
    # with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    #     pool.map(lambda _: asyncio.run(launcher()), [i for i in range(multiprocessing.cpu_count())])

    ps = []
    for i in range(multiprocessing.cpu_count()):
        ps.append(multiprocessing.Process(target=lambda: asyncio.run(launcher())))
    for p in ps:
        p.start()
    for p in ps:
        p.join()


