from Problems.Problem import Problem
from Problems.ShortestPaths.Path import Path
from Problems.ShortestPaths.Graph import Graph

"""
Tomorrow: 
1) Handle solving with constraints
2) Modify Lawler to be in line with the new design.
"""


class ShortestPathProblem(Problem):

    def __init__(self, problem_graph: Graph, source, dest):
        self.source = source
        self.dest = dest
        self.graph = problem_graph

    def __handle_constraints(self, include_constraints: set, exclude_constraints: set):
        pass

    def __get_shortest_path(self):
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {self.source: (None, 0)}
        current_node = self.source
        visited = set()

        while current_node != self.dest:
            visited.add(current_node)
            destinations = self.graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = self.graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = shortest_paths[current_node][0]
        # Reverse path
        path = path[::-1]

        return Path(path, graph.weights)

    def solve(self, include_constrains: set, exclude_constraints: set) -> Path:
        self.__handle_constraints(include_constrains, exclude_constraints)
        return self.__get_shortest_path()


if __name__ == '__main__':
    graph = Graph()
    edges = [
        ('X', 'A', 7),
        ('X', 'B', 2),
        ('X', 'C', 3),
        ('X', 'E', 4),
        ('A', 'B', 3),
        ('A', 'D', 4),
        ('B', 'D', 4),
        ('B', 'H', 5),
        ('C', 'L', 2),
        ('D', 'F', 1),
        ('F', 'H', 3),
        ('G', 'H', 2),
        ('G', 'Y', 2),
        ('I', 'J', 6),
        ('I', 'K', 4),
        ('I', 'L', 4),
        ('J', 'L', 1),
        ('K', 'Y', 5),
    ]

    for edge in edges:
        graph.add_edge(*edge)

    test = ShortestPathProblem(graph, 'X', 'D')
    best = test.solve(set(), set())
    print(best)
    print(best.score())
