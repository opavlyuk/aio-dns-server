import asyncio


class DatagramClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None
        self.reply = None

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.message)

    def datagram_received(self, data, addr):
        self.reply = data
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        self.on_con_lost.set_result(True)


async def send_dns_request(request, addr, port):
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: DatagramClientProtocol(request, on_con_lost),
        remote_addr=(addr, port))

    try:
        await on_con_lost
    finally:
        transport.close()

    return transport, protocol
