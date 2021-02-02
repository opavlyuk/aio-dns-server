from abc import ABC, abstractmethod

from dnslib import RCODE, DNSRecord

from aio_dns_server.client import send_dns_request


class AbstractBaseResolver(ABC):
    @abstractmethod
    async def resolve(self):
        return


def block_type(handler):
    

@block_type('first')(block)
def block(self):
    pass

block_type


class PyHoleResolver(AbstractBaseResolver):
    block_types = {}

    def __init__(self, upstream_addr, upstream_port=53, black_list=None, filter_func=qname.matchGlob):
        self.black_list = black_list if black_list is not None else []
        self.upstream_addr = upstream_addr
        self.upstream_port = upstream_port
        self.filter_func = filter_func


    async def resolve(self, request):
        reply = request.reply()

        if any([self.filter_func(record) for record in self.black_list]):
            reply.header.rcode = getattr(RCODE, 'NXDOMAIN')
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
