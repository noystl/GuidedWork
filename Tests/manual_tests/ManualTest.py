"""
A simple sanity check. Runs the three algorithms on a simple network (but can be modified to run with any other weighted
network by changing WEIGHTED_NET_PATH) and logs the solutions together with some extra data.
"""

import logging
import time
import util
import networkx as nx
import os
from Enumerators.Enumerator import Enumerator
from Enumerators.OriginalLawler import OriginalLawler
from Enumerators.NaiveEnumerator import NaiveEnumerator
from Enumerators.LazyEnumerator import LazyEnumerator
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem
from Problems.SolutionData import SolutionData

cur_path = os.path.dirname(__file__)
test_net_path = os.path.relpath('..\\..\\Networks\\test_net.txt', cur_path)


logging.basicConfig(filename='manual_test.log', filemode='w', level=logging.INFO)


def log_sol_data(sol_data: SolutionData):
    """
    Logs the solution and additional data (inclusion constraints, exclusion constraints, cost including penalty and
    original cost).
    """
    logging.info("solution: " + str(sol_data.solution) + " I: " + str(sol_data.include_constraints) + " E: " +
                 str(sol_data.exclude_constraints) + " cost: " + str(sol_data.solution.current_cost) +
                 " original_cost: " + str(sol_data.solution.original_cost))


def eval_alg_for_tests(alg: Enumerator, g: nx.DiGraph):
    """
    Runs the given algorithm and logs the solutions it found together with some evaluation metrics.
    :param alg: an enumeration algorithm.
    :param g: the input graph the enumerator uses.
    """
    logging.info("--------Enumerating with: " + str(type(alg).__name__) + "---------------")
    sol_gen = alg.get_solution_generator()
    total_length = 0
    edges_seen = set()
    time1 = time.time()
    for queue_elem in sol_gen:
        log_sol_data(queue_elem)
        total_length += queue_elem.solution.original_cost
        edges_seen = edges_seen.union(set(queue_elem.solution.values))
    time2 = time.time()
    logging.info('Total paths length: ' + str(total_length))
    logging.info('Average path cost: ' + str(total_length / alg.to_generate))
    logging.info('Percent of edges seen: ' + str(len(edges_seen) / g.size()))
    logging.info('Running time: ' + str((time2 - time1)) + ' s.')
    logging.info('Number of problems solved: ' + str(alg.number_of_problems_solved) + '\n')


if __name__ == '__main__':
    graph = util.generate_graph(test_net_path)
    k = 8
    src = 1  # Some node in the tested network.
    dst = 5  # Some node in the tested network.
    eval_alg_for_tests(OriginalLawler(ShortestPathProblem(graph, src, dst), k), graph)
    eval_alg_for_tests(NaiveEnumerator(ShortestPathProblem(graph, src, dst, lambda x: x * 1.2), k), graph)
    eval_alg_for_tests(LazyEnumerator(ShortestPathProblem(graph, src, dst, lambda x: x * 1.2), k), graph)
