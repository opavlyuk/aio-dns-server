from abc import abstractmethod


class AbstractBaseReporter:
    @abstractmethod
    async def report(self, **kwargs):
        pass


class MongoReporter(AbstractBaseReporter):
    def __init__(self, stats_collection):
        self.stats_collection = stats_collection

    async def report(self, **kwargs):
        result = self.stats_collection.insert_one(kwargs)
        return result
