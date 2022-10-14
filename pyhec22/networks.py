
from networkx import DiGraph, is_branching

from .exceptions import NotConfluent


def is_confluent(graph):
    return is_branching(graph.reverse())


class Network(object):

    def __init__(self, links):
        self.links = links

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        graph = DiGraph(links)
        if not is_confluent(graph):
            raise NotConfluent('Not a valid network with full confluence')
        # list(topological_sort(graph))  # Check that the tree is sortable
        self._links = links

    def check_circular_references(self):
        pass

    def check_single_descendents(self):
        pass
