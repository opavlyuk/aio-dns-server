import asyncio

from dnslib import DNSRecord


class DNSDatagramProtocol(asyncio.DatagramProtocol):
    def __init__(self, resolver, logger=None):
        self.resolver = resolver
        self.logger = logger
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        loop = asyncio.get_running_loop()
        loop.create_task(self.handle_datagram(data, addr))

    async def handle_datagram(self, data, addr):
        request = DNSRecord.parse(data)
        reply = await self.resolver.resolve(request)
        if reply is not None:
            self.transport.sendto(reply.pack(), addr)


class DNSServer:
    def __init__(self, resolver, protocol, address="0.0.0.0", port=53, loop=None):
        self.protocol = protocol
        self.address = address
        self.port = port
        self.transport_inst = None
        self.protocol_inst = None
        self.resolver = resolver
        self.loop = loop or asyncio.get_running_loop()

    async def start(self):
        self.transport_inst, self.protocol_inst = await self.loop.create_datagram_endpoint(
            lambda: self.protocol(self.resolver),
            local_addr=(self.address, self.port),
            reuse_port=True,
        )

    def stop(self):
        self.transport_inst.close()
