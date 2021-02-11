from abc import ABC, abstractmethod

from dnslib import RCODE, DNSRecord, RR

from aio_dns_server.client import send_dns_request


class AbstractBaseResolver(ABC):
    @abstractmethod
    async def resolve(self):
        return


class PyHoleResolver(AbstractBaseResolver):
    def __init__(self, upstream_addr, upstream_port=53, block_list=None):
        self.block_list = block_list if block_list is not None else []
        self.upstream_addr = upstream_addr
        self.upstream_port = upstream_port

    def _get_blocking_reply(self, request):
        reply = request.reply()
        qname = request.q.qname
        reply.add_answer(*RR.fromZone(f'{qname} 2 A 0.0.0.0'))
        reply.add_answer(*RR.fromZone(f'{qname} 2 AAAA ::'))
        return reply

    async def _query_upstream_dns(self, request):
        reply = request.reply()
        try:
            _, upstream_protocol = await send_dns_request(request.pack(), self.upstream_addr, self.upstream_port)
        except Exception:
            raise

        upstream_raw_reply = getattr(upstream_protocol, 'reply')
        if not upstream_raw_reply:
            reply.header.rcode = getattr(RCODE, 'SERVFAIL')
        else:
            reply = DNSRecord.parse(upstream_raw_reply)

        return reply

    async def resolve(self, request):
        qname = request.q.qname

        if qname.idna() in self.block_list:
            reply = self._get_blocking_reply(request)
        else:
            reply = await self._query_upstream_dns(request)

        return reply
