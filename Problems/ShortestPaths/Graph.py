from collections import defaultdict


class Graph:
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

    def remove_edge(self, from_node, to_node):
        neighbors = self.edges[from_node]
        if len(neighbors) == 0:
            del self.edges[from_node]
        else:
            neighbors.remove(to_node)
        del self.weights[(from_node, to_node)]
