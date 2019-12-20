from Problems.Problem import Problem
from Problems.SolutionData import SolutionData
from Problems.ShortestPaths.Path import Path
import copy
import networkx as nx


class ShortestPathProblem(Problem):

    def __init__(self, problem_graph: nx.DiGraph, source, dest):
        self.source = source
        self.dest = dest
        self.original_graph = problem_graph
        self.graph = copy.deepcopy(problem_graph)

    def solve(self, source_to_mid_edges: list, edges_to_delete: list):
        new_graph = copy.deepcopy(self.graph)
        new_graph.remove_edges_from(source_to_mid_edges + edges_to_delete)
        new_source = self.source if len(source_to_mid_edges) == 0 else source_to_mid_edges[-1][1]

        try:
            mid_to_dest_path = nx.algorithms.shortest_paths.weighted.dijkstra_path(new_graph, new_source, self.dest,
                                                                                   weight='weight')
        except nx.NetworkXNoPath:  # if there is no path between the source and the destination.
            return None

        mid_to_dest_edges = []
        curr = 1
        # mid_to_dest_edges = [(mid_to_dest_path[i - 1], mid_to_dest_path[i]) for i in
        #                      range(1, len(mid_to_dest_path))]
        for i in range(1, len(mid_to_dest_path)):
            mid_to_dest_edges.append((mid_to_dest_path[curr - 1], mid_to_dest_path[curr]))
            curr += 1

        best_path = Path(source_to_mid_edges + mid_to_dest_edges, self.original_graph, self.graph)
        best_path.set_unfixed_elements(mid_to_dest_edges)
        return SolutionData(best_path, source_to_mid_edges, edges_to_delete)

    def apply_penalty(self, edges: list):
        for edge in edges:
            self.graph[edge[0]][edge[1]]['weight'] += 1
