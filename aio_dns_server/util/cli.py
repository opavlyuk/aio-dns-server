import argparse


class ArgumentError(Exception):
    pass


def parse_cl_args():
    parser = argparse.ArgumentParser(description='DNS filtering proxy.')
    parser.add_argument('--address', type=str, default=None, help='Listen address.')
    parser.add_argument('--port', type=int, default=None, help='Listen port.')
    parser.add_argument('--upstream_dns_addr', type=str, default=None, help='Address of the upstream DNS server')
    parser.add_argument('--upstream_dns_port', type=int, default=None, help='Port of the upstream DNS server')
    parser.add_argument('--block_list', type=str, default=None, help='Path to the file with block list.')
    # MongoDB args
    parser.add_argument('--mongo_addr', type=str, default=None, help='MongoDB server address.')
    parser.add_argument('--mongo_db_name', type=str, default=None, help='Database name.')
    parser.add_argument('--mongo_collection_name', type=str, default=None, help='Main collection name.')
    args = parser.parse_args()
    return args
