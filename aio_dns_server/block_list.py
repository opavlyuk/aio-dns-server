from abc import ABC, abstractmethod
from pathlib import Path

END_OF_DOMAIN = None


class AbstractBlockList(ABC):
    @abstractmethod
    def __contains__(self, item):
        pass


class BlockList(AbstractBlockList):
    def __init__(self, block_list_path):
        self.block_list_path = Path(block_list_path)
        self._search_tree = self._make_search_tree()

    def _make_search_tree(self):
        tree = {}
        with self.block_list_path.open('r') as block_list:
            for l in block_list:
                subtree = tree
                labels = l.strip().split('.')
                for label in labels[::-1]:
                    subtree = subtree.setdefault(label, {})
                else:
                    subtree[END_OF_DOMAIN] = END_OF_DOMAIN
        return tree

    def __contains__(self, item):
        labels = item.split('.')[:-1]
        if labels[0] == 'www':
            del labels[0]
        subtree = self._search_tree
        for label in labels[::-1]:
            match = subtree.get(label)
            if match is END_OF_DOMAIN:
                return False
            subtree = match
        if END_OF_DOMAIN in match:
            return True
        return False
