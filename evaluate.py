import random
from Problems.ShortestPaths.Graph import Graph
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem
from Enumerators.OriginalLawler import OriginalLawler
from Enumerators.DiverseLawler import DiverseLawler
from Enumerators.LazyDiverseLawler import LazyDiverseLawler
from Enumerators.Enumerator import Enumerator

NETWORK_PATH = 'Networks\web-Stanford.txt'
WEIGHTED_NET_FILE_NAME = 'weighted_net.txt'


def add_weights(net_path: str, smallest_weight: int, largest_weight: int):
    print("Adding weights...")
    with open(WEIGHTED_NET_FILE_NAME, 'w') as weighted_net:
        with open(net_path, 'r') as original_net:
            for line in original_net:
                if not line.startswith('#'):
                    weight = random.randint(smallest_weight, largest_weight)
                    weighted_net.write(line.rstrip('\n') + "\t" + str(weight) + '\n')


def generate_graph() -> Graph:
    print("Generating network graph...")
    net_graph = Graph()
    with open(WEIGHTED_NET_FILE_NAME, 'r') as network_file:
        for line in network_file:
            line_data = line.rstrip('\n').split("\t")
            net_graph.add_edge(line_data[0], line_data[1], int(line_data[2]))
    return net_graph


def test_alg(alg: Enumerator):
    print("Enumerating...")
    sol_gen = alg.get_solution_generator()
    for sol_data in sol_gen:
        print("solution: " + str(sol_data.solution) + " I: " + str(sol_data.include_constraints) + " E: " +
              str(sol_data.exclude_constraints) + " score: " + str(sol_data.solution.updated_score()) +
              " original_score: " + str(sol_data.solution.original_score()))


if __name__ == '__main__':
    add_weights(NETWORK_PATH, 2, 10)
    graph = generate_graph()
    problem = ShortestPathProblem(graph, '1', '6548')
    test_alg(OriginalLawler(problem, 3))
    # apply algorithms on the network
    # write logs to file: paths discovered, score, I, E etc.
    # measure time, diversification and paths length.
    # print results.
    # delete helper files etc.
    pass
