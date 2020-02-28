from Problems.Solution import Solution
import networkx as nx


class Path(Solution):
    """
    Represents a solution to the shortest path problem.
    """

    def __init__(self, values: list, original_net: nx.DiGraph, updated_net: nx.DiGraph):
        super().__init__(values)
        self.original_net = original_net                          # The original network, no penalty.
        self.updated_net = updated_net                            # The current network (including penalty).
        self.original_cost = self.get_original_cost()             # The original cost of this path (no penalty).
        self.current_cost = self.get_updated_cost()               # The current cost of this path (with penalty)
        self.current_weights = self.get_current_weights()         # Records the weights this path had when
                                                                  # current_score was calculated.

    def get_current_weights(self) -> dict:
        """
        Gets the most updated weights for the edges of this path.
        :return: a dictionary of the form: {edge: weight}
        """
        curr_weights = {}
        for edge in self.values:
            curr_weights[edge] = self.updated_net[edge[0]][edge[1]]['weight']
        return curr_weights

    def get_original_cost(self) -> float:
        """
        Gets the cost of this path, without penalty.
        """
        cost = 0
        for edge in self.values:
            cost += self.original_net[edge[0]][edge[1]]['weight']
        return cost

    def get_updated_cost(self) -> float:
        """
        Gets the most updated cost of this path (including penalty).
        """
        cost = 0
        for edge in self.values:
            cost += self.updated_net[edge[0]][edge[1]]['weight']
        return cost

    def get_updated_values(self) -> set:
        """
        Gets the elements of this path who's cost was updated since the last time the cost of this path was updated.
        """
        updated = set()
        for edge in self.values:
            if self.current_weights[edge] != self.updated_net[edge[0]][edge[1]]['weight']:
                updated.add(edge)
        return updated

    def update(self):
        """
        Updates the cost of this path.
        """
        self.current_cost = self.get_updated_cost()
        self.current_weights = self.get_current_weights()

    def __str__(self):
        """
        Returns a string representation of this path.
        """
        return str(self.values)
