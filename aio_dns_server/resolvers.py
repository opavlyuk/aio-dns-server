from abc import ABC, abstractmethod

from dnslib import RCODE, DNSRecord, RR

from aio_dns_server.client import send_dns_request


class AbstractBaseResolver(ABC):
    @abstractmethod
    async def resolve(self):
        return


class PyHoleResolver(AbstractBaseResolver):
    def __init__(self, upstream_addr, upstream_port=53, black_list=None, filter_func=None):
        self.black_list = black_list if black_list is not None else []
        self.upstream_addr = upstream_addr
        self.upstream_port = upstream_port
        self.filter_func = filter_func

    async def resolve(self, request):
        reply = request.reply()
        qname = request.q.qname
        filter_func = lambda record: qname.matchGlob(record) if self.filter_func is None else self.filter_func

        if any([filter_func(record) for record in ('*ukr.net*',)]):
            reply
            reply.add_answer(*RR.fromZone(f'{qname} 2 A 0.0.0.0'))
            reply.add_answer(*RR.fromZone(f'{qname} 2 AAAA ::'))
            return reply

        try:
            _, up_protocol = await send_dns_request(request.pack(), self.upstream_addr, self.upstream_port)
        except Exception:
            raise

        upstream_raw_reply = getattr(up_protocol, 'reply')
        if not upstream_raw_reply:
            reply.header.rcode = getattr(RCODE, 'SERVFAIL')
        else:
            reply = DNSRecord.parse(upstream_raw_reply)
        return reply
