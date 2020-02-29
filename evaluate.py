"""
This module is used to evaluate the performances and solution quality of the three enumerators.
The results appear in evaluate.log
"""

import time
import networkx as nx
import logging
import util
import matplotlib.pyplot as plt
import numpy as np
from Enumerators.Enumerator import Enumerator
from Enumerators.OriginalLawler import OriginalLawler
from Enumerators.NaiveEnumerator import NaiveEnumerator
from Enumerators.LazyEnumerator import LazyEnumerator
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem
from Problems.Solution import Solution

NETWORK_PATH = 'Networks\\roadNet-PA.txt'  # The path of the inspected network (no weights).
WEIGHTED_NET_PATH = 'Networks\\weighted_net.txt'  # The path of the inspected network after weights were added.
META_PREFIX = '#'

logging.basicConfig(filename='evaluate.log', filemode='w', level=logging.INFO)


def jaccard_dist(set1: set, set2: set) -> float:
    """
    Calculates the Jaccard Distance between two sets.
    """
    return 1 - (len(set1.intersection(set2)) / len(set1.union(set2)))


def path_replacement_dist(set1: set, set2: set) -> float:
    """
    Calculated the path-replacement distance between two sets.
    """
    return len(set1.difference(set2)) / len(set1)


def is_different(solutions: list, new_sol: Solution, thresh: float, dist_func) -> bool:
    """
    Tests whether new_sol is "significantly different" from what's already in solutions.
    :param solutions: the "significantly different" solutions collected until now.
    :param new_sol: a candidate to the significantly different solutions list.
    :param thresh: a thresh for the distance function.
    :param dist_func: The distance function used for the evaluation.
    :return: True if for each solution s in solutions, distance(s, new_sol) >= thresh.
    """
    new_sol_values = set(new_sol.values)
    for sol in solutions:
        if dist_func(set(sol.values), new_sol_values) < thresh:
            return False
    return True


def count_different_solutions(solutions, thresholds: list):
    """
    Counts how many significantly different solutions exists using two distance functions:
    1) Jaccard Distance
    2) Path-replacement distance
    with different thresholds.
    :param solutions: all of the solutions a certain enumerator had found.
    :param thresholds: the thresholds for the distance functions.
    """
    different_solutions_jaccard = []
    different_solutions_path_replacement = []

    for thresh in thresholds:
        for sol_data in solutions:
            sol = sol_data.solution

            if is_different(different_solutions_jaccard, sol, thresh, jaccard_dist):
                different_solutions_jaccard.append(sol)

            if is_different(different_solutions_path_replacement, sol, thresh, path_replacement_dist):
                different_solutions_path_replacement.append(sol)

        logging.info('Percentage of different solutions, Jaccard difference, t = ' + str(thresh) + ': ' +
                     str(len(different_solutions_jaccard) / len(solutions)))
        logging.info('Percentage of different solutions, path-replacement difference, t = ' + str(thresh) + ': ' +
                     str(len(different_solutions_path_replacement) / len(solutions)))

        different_solutions_jaccard = []
        different_solutions_path_replacement = []


def eval_paths_quality(solutions: list):
    """
    Calculates the total length and average cost of the paths in solutions.
    :param solutions: A list of solutions (paths).
    """
    total_length = 0
    for sol_data in solutions:
        total_length += sol_data.solution.original_cost
    logging.info('Total paths length: ' + str(total_length))
    logging.info('Average path cost: ' + str(total_length / len(solutions)))


def calc_percentage_of_edges(solutions: list, net: nx.DiGraph):
    """
    Calculates the ratio between the number of different edges that appear in the solutions set to the total
    number of different edges in the graph.
    :param solutions: a list of solutions (paths).
    :param net: The tested network graph.
    """
    edges_seen = set()
    for sol_data in solutions:
        edges_seen = edges_seen.union(set(sol_data.solution.values))

    logging.info('Percent of edges seen: ' + (str(len(edges_seen) / net.size())))


def eval_sols(alg: Enumerator, net: nx.DiGraph):
    """
    Evaluate the solutions quality of the given enumerator, and writes the results to evaluate.log
    :param alg: one of the evaluated enumerators.
    :param net: the examined network.
    """
    logging.info("--------Evaluating: " + str(type(alg).__name__) + "---------------")
    solutions = list(alg.get_solution_generator())

    # Paths quality evaluation:
    eval_paths_quality(solutions)

    # Diversity evaluation:
    calc_percentage_of_edges(solutions, net)
    count_different_solutions(solutions, [0.25, 0.5, 0.75])

    logging.info('\n')


def eval_time(alg: Enumerator) -> list:
    """
    Returns a list where list[i] is the time (in seconds) it took to generate solution i, and prints the total running
    time of the algorithm to the log file.
    :param alg: the enumerator to evaluate.
    :return: a list of solutions generation times.
    """
    sol_gen = alg.get_solution_generator()
    time1 = time.time()
    times = [0]
    for _ in sol_gen:
        times.append(time.time() - time1)
    time2 = time.time()
    logging.info('Running time (' + str(type(alg).__name__) + '): ' + str((time2 - time1)) + ' s.')
    return times


def plot_times(orig_alg_times: list, naive_alg_times: list, lazy_alg_times: list):
    """
    Plots the time it took to generate the k-th solution in a single run, for 1<=k<=50.
    :param orig_alg_times: the times recorded for Lawler's algorithm.
    :param naive_alg_times: the times recorded for the naive variant.
    :param lazy_alg_times: the times recorded for the lazy variant.
    """
    fig, ax = plt.subplots()
    plt.xlabel('k')
    plt.ylabel('time(sec)')
    xs_range = np.arange(len(orig_alg_times))
    ax.plot(xs_range, orig_alg_times, label="Original")
    ax.plot(xs_range, naive_alg_times, label="Naive")
    ax.plot(xs_range, lazy_alg_times, label="Lazy")
    ax.legend()
    plt.show()


if __name__ == '__main__':
    """
    Evaluates the enumerating algorithms and print the results to evaluate.log
    """
    # util.add_weights(NETWORK_PATH, 1, 1)
    graph = util.generate_graph(WEIGHTED_NET_PATH)
    k = 50
    src = 2             # Some node in the tested network.
    dst = 150           # Some node in the tested network.

    logging.info("-------- Evaluating Running Times ---------------")
    orig_times = eval_time(OriginalLawler(ShortestPathProblem(graph, src, dst), k))
    naive_times = eval_time(NaiveEnumerator(ShortestPathProblem(graph, src, dst, lambda x: x * 1.2), k))
    lazy_times = eval_time(LazyEnumerator(ShortestPathProblem(graph, src, dst, lambda x: x * 1.2), k))
    plot_times(orig_times, naive_times, lazy_times)

    logging.info("-------- Evaluating Solutions Quality --------------- \n")
    eval_sols(OriginalLawler(ShortestPathProblem(graph, src, dst), k), graph)
    penalty_funcs = [lambda x: x + 1, lambda x: x * 1.2, lambda x: x * (x + 1)]
    for penalty_func in penalty_funcs:
        eval_sols(LazyEnumerator(ShortestPathProblem(graph, src, dst, penalty_func), k), graph)
