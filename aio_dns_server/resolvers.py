from abc import ABC, abstractmethod

from dnslib import RCODE, DNSRecord, RR

from aio_dns_server.client import send_dns_request


class AbstractBaseResolver(ABC):
    @abstractmethod
    async def resolve(self):
        return


class FilterResolver(AbstractBaseResolver):
    class StatusCodes:
        blocked = 0
        allowed = 1
        serv_fail = 2

    def __init__(self, upstream_addr, upstream_port=53, block_list=None):
        self.block_list = block_list if block_list is not None else []
        self.upstream_addr = upstream_addr
        self.upstream_port = upstream_port

    def _get_blocking_reply(self, request, reply):
        reply.extra['status'] = self.StatusCodes.blocked
        qname = request.q.qname
        reply.add_answer(*RR.fromZone(f'{qname} 2 A 0.0.0.0'))
        reply.add_answer(*RR.fromZone(f'{qname} 2 AAAA ::'))
        return reply

    async def _query_upstream_dns(self, request, reply):
        try:
            _, upstream_protocol = await send_dns_request(request.pack(), self.upstream_addr, self.upstream_port)
        except Exception:
            raise

        upstream_raw_reply = getattr(upstream_protocol, 'reply')
        if not upstream_raw_reply:
            reply.header.rcode = getattr(RCODE, 'SERVFAIL')
            reply.extra['status'] = self.StatusCodes.serv_fail
        else:
            reply = DNSRecord.parse(upstream_raw_reply)
            reply.extra = {}
            reply.extra['status'] = self.StatusCodes.allowed

        return reply

    async def resolve(self, request):
        reply = request.reply()
        reply.extra = {}
        qname = request.q.qname

        if qname.idna() in self.block_list:
            reply = self._get_blocking_reply(request, reply)
        else:
            reply = await self._query_upstream_dns(request, reply)

        return reply
