from Problems.Problem import Problem
from Problems.SolutionData import SolutionData
from Problems.ShortestPaths.Path import Path
import copy
import math
import time
import networkx as nx


class ShortestPathProblem(Problem):

    def __init__(self, problem_graph: nx.DiGraph, source, dest):
        self.source = source
        self.dest = dest
        self.original_graph = problem_graph
        self.graph = copy.deepcopy(problem_graph)
        print(self.graph.number_of_nodes())
        # self.prune_graph()
        print(self.graph.number_of_nodes())

    def prune_graph(self):
        distances = nx.algorithms.shortest_paths.weighted.single_source_dijkstra_path_length(self.graph, self.source)
        optimal_dist = distances[self.dest]
        to_rem = [node for node in distances if distances[node] > optimal_dist * 5]
        self.graph.remove_nodes_from(to_rem)

    def save_weights(self, to_save: list) -> dict:
        saved_weights = {}
        for edge in to_save:
            saved_weights[edge] = self.graph[edge[0]][edge[1]]['weight']
        return saved_weights

    def apply_constraints(self, banned_edges: list):
        for edge in banned_edges:
            self.graph[edge[0]][edge[1]]['weight'] = math.inf

    def retrieve_weights(self, saved_weights: dict):
        for edge in saved_weights:
            self.graph[edge[0]][edge[1]]['weight'] = saved_weights[edge]

    def find_shortest_path(self, source: int):
        try:
            path = nx.algorithms.shortest_paths.weighted.dijkstra_path(self.graph, source, self.dest,
                                                                       weight='weight')
        except nx.NetworkXNoPath:  # if there is no path between the source and the destination.
            return None

        return [(path[i - 1], path[i]) for i in range(1, len(path))]

    def is_finite_solution(self, edges: list):
        for edge in edges:
            if self.graph[edge[0]][edge[1]]['weight'] is math.inf:
                return False
        return True

    def solve(self, source_to_mid_edges: list, edges_to_delete: list):
        saved_weights = self.save_weights(source_to_mid_edges + edges_to_delete)
        self.apply_constraints(source_to_mid_edges + edges_to_delete)
        new_source = self.source if len(source_to_mid_edges) == 0 else source_to_mid_edges[-1][1]
        time1 = time.time()
        mid_to_dest_edges = self.find_shortest_path(new_source)
        time2 = time.time()
        print('Dijkstra time: ' + str(time2 - time1))
        if mid_to_dest_edges and self.is_finite_solution(mid_to_dest_edges):
            self.retrieve_weights(saved_weights)
            best_path = Path(source_to_mid_edges + mid_to_dest_edges, self.original_graph, self.graph)
            best_path.set_unfixed_elements(mid_to_dest_edges)

            return SolutionData(best_path, source_to_mid_edges, edges_to_delete)

        self.retrieve_weights(saved_weights)
        return None

    def apply_penalty(self, edges: list):
        for edge in edges:
            self.graph[edge[0]][edge[1]]['weight'] *= 1.3
