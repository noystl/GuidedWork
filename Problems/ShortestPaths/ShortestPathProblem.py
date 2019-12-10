from Problems.Problem import Problem
from Problems.SolutionData import SolutionData
from Problems.ShortestPaths.Path import Path
from Problems.ShortestPaths.Graph import Graph
import copy


class ShortestPathProblem(Problem):

    def __init__(self, problem_graph: Graph, source, dest):
        self.source = source
        self.dest = dest
        self.graph = problem_graph

    def __delete_edges(self, edges_to_delete: list) -> Graph:
        new_graph = copy.deepcopy(self.graph)
        for e in edges_to_delete:
            new_graph.remove_edge(e[0], e[1])
        return new_graph

    def __get_shortest_path(self, g: Graph, source) -> list:
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {source: (None, 0)}
        current_node = source
        visited = set()

        while current_node != self.dest:
            visited.add(current_node)
            destinations = g.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = g.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return []
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = shortest_paths[current_node][0]
        # Reverse path
        path = path[::-1]

        return path

    def solve(self, source_to_mid_edges: list, edges_to_delete: list):
        new_graph = self.__delete_edges(source_to_mid_edges + edges_to_delete)
        new_source = self.source if len(source_to_mid_edges) == 0 else source_to_mid_edges[-1][1]
        mid_to_dest_path = self.__get_shortest_path(new_graph, new_source)
        mid_to_dest_edges = []
        if len(mid_to_dest_path) > 0:
            curr = 1
            for i in range(1, len(mid_to_dest_path)):
                mid_to_dest_edges.append((mid_to_dest_path[curr - 1], mid_to_dest_path[curr]))
                curr += 1
        else:
            return None
        best_path = Path(source_to_mid_edges + mid_to_dest_edges, self.graph.weights)
        best_path.set_unfixed_elements(mid_to_dest_edges)
        return SolutionData(best_path, source_to_mid_edges, edges_to_delete)

    def apply_penalty(self, occurrences: dict):
        for edge in occurrences:
            self.graph.weights[edge] += 2
