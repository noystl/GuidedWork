import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import logging
from Enumerators.Enumerator import Enumerator
from Enumerators.OriginalLawler import OriginalLawler
from Enumerators.DiverseLawler import DiverseLawler
from Enumerators.LazyDiverseLawler import LazyDiverseLawler
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem
from Problems.SolutionData import SolutionData

NETWORK_PATH = 'Networks\\roadNet-PA.txt'
WEIGHTED_NET_PATH = 'Networks\weighted_net.txt'
logging.basicConfig(filename='evaluate.log', filemode='w', level=logging.INFO)


def add_weights(net_path: str, smallest_weight: int, largest_weight: int):
    print("Adding weights...")
    with open(WEIGHTED_NET_PATH, 'w') as weighted_net:
        with open(net_path, 'r') as original_net:
            for line in original_net:
                if not line.startswith('#'):
                    weight = random.randint(smallest_weight, largest_weight)
                    weighted_net.write(line.rstrip('\n') + "\t" + str(weight) + '\n')


def generate_graph() -> nx.DiGraph:
    logging.info("Generating network graph...")
    net_graph = nx.read_edgelist(WEIGHTED_NET_PATH, nodetype=int,
                                 data=(('weight', float),), create_using=nx.DiGraph())
    return net_graph


def log_sol_data(sol_data: SolutionData):
    logging.info("solution: " + str(sol_data.solution) + " I: " + str(sol_data.include_constraints) + " E: " +
                 str(sol_data.exclude_constraints) + " score: " + str(sol_data.solution.current_score) +
                 " original_score: " + str(sol_data.solution.original_score))


def eval_alg(alg: Enumerator, graph: nx.DiGraph):
    logging.info("--------Enumerating with: " + str(type(alg).__name__) + "---------------")
    sol_gen = alg.get_solution_generator()
    total_length = 0
    edges_seen = set()
    time1 = time.time()
    for sol_data in sol_gen:
        log_sol_data(sol_data)
        total_length += sol_data.solution.original_score
        edges_seen = edges_seen.union(set(sol_data.solution.values))
    time2 = time.time()
    logging.info('Total paths length: ' + str(total_length))
    logging.info('Edges Seen: ' + str(len(edges_seen)) + ' out of ' + str(graph.size()))
    logging.info('Running time: ' + str((time2 - time1)) + ' s.')
    logging.info('Number of problems solved: ' + str(alg.number_of_problems_solved) + '\n')


if __name__ == '__main__':
    # add_weights(NETWORK_PATH, 1, 1)
    graph = generate_graph()
    wanted_solution_number = 50
    src = 2
    dst = 153
    eval_alg(OriginalLawler(ShortestPathProblem(graph, src, dst), wanted_solution_number), graph)
    # eval_alg(DiverseLawler(ShortestPathProblem(graph, src, dst), wanted_solution_number), graph)
    eval_alg(LazyDiverseLawler(ShortestPathProblem(graph, src, dst), wanted_solution_number), graph)
