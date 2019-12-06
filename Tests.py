from Enumerators.Enumerator import Enumerator
from Enumerators.LawlerEnumerator import LawlerEnumerator
from Problems.ShortestPaths.Graph import Graph
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem


def print_solutions(enumerator: Enumerator):
    for solution_data in enumerator.get_solution_generator():
        pass
        print("solution: " + str(solution_data.solution) + " I: " + str(solution_data.include_constraints) + " E: " +
              str(solution_data.exclude_constraints) + " score: " + str(solution_data.solution.score()))


def init_test_graph() -> Graph:
    test_graph = Graph()
    edges = [('1', '2', 1),
             ('1', '3', 1),
             ('1', '5', 9),
             ('2', '3', 1),
             ('2', '5', 3),
             ('3', '4', 2),
             ('3', '5', 1),
             ('4', '5', 2)
             ]

    for edge in edges:
        test_graph.add_edge(*edge)
    return test_graph


if __name__ == '__main__':
    graph = init_test_graph()
    original = LawlerEnumerator(ShortestPathProblem(graph, '1', '5'))
    print("-----------ORIGINAL LAWLER--------------")
    print_solutions(original)
    # print("-----------DIVERSE LAWLER---------------")
    # naive_diverse = DiverseEnumerator(ShortestPathProblem(graph, '1', '5'))
    # print_solutions(naive_diverse)