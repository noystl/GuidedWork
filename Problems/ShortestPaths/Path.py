from Problems.Solution import Solution
import networkx as nx


class Path(Solution):
    def __init__(self, values: list, original_net: nx.DiGraph, updated_net: nx.DiGraph):
        super().__init__(values)
        self.original_net = original_net
        self.updated_net = updated_net
        self.original_score = self.get_original_score()
        self.current_score = self.get_updated_score()

    def get_original_score(self):
        score = 0
        for edge in self.values:
            score += self.original_net[edge[0]][edge[1]]['weight']
        return score

    def get_updated_score(self):
        score = 0
        for edge in self.values:
            score += self.updated_net[edge[0]][edge[1]]['weight']
        return score

    def __str__(self):
        return str(self.values)
