
from networkx import DiGraph, is_branching, topological_sort

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
        self._links = links

    '''
    def get_results(self, basin_flow):
        links = self.links
        graph = DiGraph(links)
        sorted_gutters = topological_sort(graph)
        results = []
        for g in sorted_gutters:
            r = {
                "gutter": g,
                "basin_flow": basin_flow,
                "upstream_flow": 0.0,
                "total_flow": 0.0,
                "interecepted_flow": 0.0,
                "bypass_flow": 0.0
            }
            for link_g, bypass_g in links:
                if g == link_g:
                    r["bypass_gutter"] = links.pop(bypass_g)
                    break
            results.append(r)
        for r in results:
            g = r["gutter"]
            upstream_flow = r["upstream_flow"]
            total_flow = upstream_flow + basin_flow
            intercept = g.inlet.intercepted(total_flow) if g.inlet else 0.0
            bypass_flow = total_flow - intercept
            r["total_flow"] = total_flow
            r["intercepted_flow"] = intercept
            r["bypass_flow"] = bypass_flow
            bypass_gutter = r["bypass_gutter"]
            for r2 in results:
                if r2["guttter"] == bypass_gutter:
                    r2["upstream_flow"] += bypass_flow

        return results
    '''
