import asyncio

from dnslib import DNSRecord


class DNSDatagramProtocol(asyncio.DatagramProtocol):
    def __init__(self, resolver, logger=None):
        self.resolver = resolver
        self.logger = logger
        self.transport = None

    def connection_made(self, transport):
        print('Connection made')
        self.transport = transport

    def datagram_received(self, data, addr):
        print('incoming')
        loop = asyncio.get_running_loop()
        loop.create_task(self.handle_datagram(data, addr))

    async def handle_datagram(self, data, addr):
        request = DNSRecord.parse(data)
        reply = await self.resolver.resolve(request)
        if reply is not None:
            self.transport.sendto(reply.pack(), addr)
        print('outgoing')


class DNSServer:
    def __init__(self, resolver, address="0.0.0.0", port=53, protocol=None):
        self.protocol = protocol
        self.address = address
        self.port = port
        self.transport_inst = None
        self.protocol_inst = None
        self.resolver = resolver

    async def start(self):
        loop = asyncio.get_running_loop()
        self.transport_inst, self.protocol_inst = await loop.create_datagram_endpoint(
            lambda: self.protocol(self.resolver),
            local_addr=(self.address, self.port),
            reuse_port=True,
        )

    async def stop(self):
        self.transport_inst.close()
