import asyncio
import datetime
from ipaddress import ip_address

from dnslib import DNSRecord


class DNSDatagramProtocol(asyncio.DatagramProtocol):
    def __init__(self, resolver, reporter):
        self.resolver = resolver
        self.reporter = reporter
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        loop = asyncio.get_running_loop()
        loop.create_task(self.handle_datagram(data, addr))

    async def handle_datagram(self, data, addr):
        in_ts = datetime.datetime.utcnow()
        request = DNSRecord.parse(data)
        reply = await self.resolver.resolve(request)
        if reply is not None:
            self.transport.sendto(reply.pack(), addr)
        await self.reporter.report(
            in_ts=in_ts,
            out_ts=datetime.datetime.utcnow(),
            client_addr=int(ip_address(addr[0])),
            qname=request.q.qname.idna(),
            qtype=str(request.q.qtype),
            qclass=str(request.q.qclass),
            **reply.extra,
        )


class DNSServer:
    def __init__(self, resolver, protocol, reporter, address="0.0.0.0", port=53, loop=None):
        self.protocol = protocol
        self.address = address
        self.port = port
        self.transport_inst = None
        self.protocol_inst = None
        self.resolver = resolver
        self.reporter = reporter
        self.loop = loop or asyncio.get_running_loop()

    async def start(self):
        self.transport_inst, self.protocol_inst = await self.loop.create_datagram_endpoint(
            lambda: self.protocol(self.resolver, self.reporter),
            local_addr=(self.address, self.port),
        )

    def stop(self):
        self.transport_inst.close()
