import asyncio

import motor.motor_asyncio

from aio_dns_server.block_list import BlockList
from aio_dns_server.resolvers import FilterResolver
from aio_dns_server.server import DNSServer, DNSDatagramProtocol
from aio_dns_server.util.cli import parse_cl_args
from aio_dns_server.util.config_mgr import get_config
from aio_dns_server.util.reporter import MongoReporter


def _update_config(config, args):
    main_cfg = config['main']
    mongo_cfg = config['mongo']
    cli_args = parse_cl_args()
    for field in 'address', 'port', 'upstream_dns_addr', 'upstream_dns_port', 'block_list':
        cli_arg = getattr(cli_args, field)
        if cli_arg is not None:
            main_cfg[field] = cli_arg

    mongo_cfg['address'] = cli_args.mongo_addr if cli_args.mongo_addr is not None else mongo_cfg['address']
    mongo_cfg['db_name'] = cli_args.mongo_db_name if cli_args.mongo_addr is not None else mongo_cfg['db_name']
    mongo_cfg['stats_collection'] = cli_args.mongo_collection_name if cli_args.mongo_addr is not None else mongo_cfg[
        'stats_collection']
    return config


async def launcher():
    # Update config settings with CLI args
    config = get_config()
    config = _update_config(config, parse_cl_args())

    upstream_dns = config['main']['upstream_dns_addr']
    upstream_port = config['main']['upstream_dns_port']
    block_list = BlockList(config['main']['block_list'])
    resolver = FilterResolver(upstream_dns, upstream_port, block_list=block_list)

    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(config['mongo']['address'])
    db = mongo_client[config['mongo']['db_name']]
    stats_collection = db[config['mongo']['stats_collection']]
    reporter = MongoReporter(stats_collection)

    server = DNSServer(address=config['main']['address'], port=config['main']['port'],
                       resolver=resolver, protocol=DNSDatagramProtocol, reporter=reporter)
    await server.start()

    return server


def main():
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(launcher())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.stop()
