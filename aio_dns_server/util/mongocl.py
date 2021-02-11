import motor.motor_asyncio

from aio_dns_server.util.config_mgr import config


mongo_config = config['mongo']
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_config['address'])

cqa_metrics_db = mongo_client[mongo_config['db_name']]
cqa_metrics_collection = cqa_metrics_db[mongo_config['metrics_collection_name']]
