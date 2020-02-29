from Problems.Problem import Problem
from Problems.SolutionData import SolutionData
from Problems.ShortestPaths.Path import Path
import copy
import networkx as nx


PRUNING_FACTOR = 1.5


class ShortestPathProblem(Problem):
    """
    Represents the shortest path optimization problem (on directed graphs).
    """

    def __init__(self, problem_graph: nx.DiGraph, source, dest, penalty_func=lambda x: x):
        super().__init__(penalty_func)
        self.source = source
        self.dest = dest
        self.original_graph = problem_graph  # The original problem graph (no penalty).
        self.graph = copy.deepcopy(problem_graph)  # The problem graph (with penalty).
        self.prune_graph()

    def prune_graph(self):
        """
        Finds the nodes who's distance from the source node is greater then PRUNING_FACTOR * optimal distance, and
        removes them from self.graph
        """
        distances = nx.algorithms.shortest_paths.weighted.single_source_dijkstra_path_length(self.graph, self.source)
        optimal_dist = distances[self.dest]
        to_rem = [node for node in distances if distances[node] > optimal_dist * 1.5]
        self.graph.remove_nodes_from(to_rem)

    def find_shortest_path(self, source: int):
        """
        Uses Dijkstra to find the shortest path from source to self.destination.
        :param source: a node in self.graph
        :return: a list of the path's edges, or None if a path from source to self.dest doesn't exists.
        """
        try:
            path = nx.algorithms.shortest_paths.weighted.dijkstra_path(self.graph, source, self.dest,
                                                                       weight='weight')
        except nx.NetworkXNoPath:  # if there is no path between the source and the destination.
            return None

        return [(path[i - 1], path[i]) for i in range(1, len(path))]

    def save_edges(self, to_save: list) -> list:
        """
        Copy the edges in to_save and their weights, and returns a dictionary of the form {edge: weight}
        :param to_save: a list of edges.
        """
        saved_edges = []
        for edge in to_save:
            u, v = edge[0], edge[1]
            saved_edges.append((u, v, self.graph[u][v]['weight']))
        return saved_edges

    def solve(self, source_to_mid_edges: list, edges_to_delete: list):
        """
        Finds the shortest path under constraints.
        :param source_to_mid_edges: the edges that the path should begin with.
        :param edges_to_delete: the edges the path must not contain.
        :return: A SolutionData object, corresponding to the path that was found. If there is
        no solution under the given constraints, returns None.
        """
        saved_edges = self.save_edges(source_to_mid_edges + edges_to_delete)
        self.graph.remove_edges_from(source_to_mid_edges + edges_to_delete)
        new_source = self.source if len(source_to_mid_edges) == 0 else source_to_mid_edges[-1][1]
        mid_to_dest_edges = self.find_shortest_path(new_source)

        if mid_to_dest_edges:
            self.graph.add_weighted_edges_from(saved_edges)
            best_path = Path(source_to_mid_edges + mid_to_dest_edges, self.original_graph, self.graph)
            best_path.set_unfixed_elements(mid_to_dest_edges)
            return SolutionData(best_path, source_to_mid_edges, edges_to_delete)

        self.graph.add_weighted_edges_from(saved_edges)
        return None

    def apply_penalty(self, edges: list):
        """
        Increases the cost of the edges in to_penalize according to self.penalty_function.
        """
        for edge in edges:
            self.graph[edge[0]][edge[1]]['weight'] = self.penalty_func(self.graph[edge[0]][edge[1]]['weight'])
