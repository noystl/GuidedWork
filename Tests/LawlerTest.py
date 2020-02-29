import unittest
import logging
from Enumerators.OriginalLawler import OriginalLawler
from Problems.SolutionData import SolutionData
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem
import networkx as nx

logging.basicConfig(filename='test_results.log', filemode='w', level=logging.INFO)


class Networks:
    def __init__(self):
        self.line = self.setup_line()
        self.square = self.setup_square()
        self.diamonds = self.setup_diamonds()

    def setup_line(self) -> nx.DiGraph:
        #
        # [1]-----w=7------->[2]
        #
        line = nx.DiGraph()
        line.add_weighted_edges_from([(1, 2, 7)])
        return line

    def setup_square(self) -> nx.DiGraph:
        # [1]---------->[2]
        # ^  \           ^
        # |      \       |
        # |         \    |
        # |            \ |
        # [4]---------->[5]
        square = nx.DiGraph()
        square.add_weighted_edges_from([(1, 2, 1),
                                        (1, 5, 1),
                                        (4, 1, 2),
                                        (4, 5, 4),
                                        (5, 2, 1)])
        return square

    def setup_diamonds(self) -> nx.DiGraph:
        # [1]---------->[2]
        #    \           |
        #        \       |
        #           \    |
        #              \ v
        #               [6]------------>[5]
        #                 |  \            |
        #                 |    \ ----     |
        #                 v           \   v
        #                [3]----------->[4]
        diamonds = nx.DiGraph()
        diamonds.add_weighted_edges_from([(1, 2, 1),
                                          (1, 6, 1),
                                          (2, 6, 1),
                                          (6, 5, 1),
                                          (6, 3, 1),
                                          (6, 4, 1),
                                          (3, 4, 1),
                                          (5, 4, 1)])
        return diamonds


class TestShortestPath(unittest.TestCase):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.enumerator = OriginalLawler
        self.nets = Networks()

    def log_test_name(self, test_name: str):
        logging.info('[%s] Testing %s with %s', self.__class__.__name__, test_name, self.enumerator.__name__)

    def log_sol_data(self, sol_data: SolutionData):
        logging.info("solution: " + str(sol_data.solution) + " I: " + str(sol_data.include_constraints) + " E: " +
                     str(sol_data.exclude_constraints) + " cost: " + str(sol_data.solution.current_cost) +
                     " original_cost: " + str(sol_data.solution.original_cost))

    def check_answers(self, sol_gen, expected_outputs):
        for sol_data in sol_gen:
            self.log_sol_data(sol_data)
            expected_values = next(expected_outputs)
            self.assertEqual(sol_data.solution.values, expected_values)

    def test_line(self):
        self.log_test_name('line')
        problem = ShortestPathProblem(self.nets.line, 1, 2)
        expected_solutions = iter([[(1, 2)]])
        self.check_answers(self.enumerator(problem, 1).get_solution_generator(), expected_solutions)

    def test_square(self):
        self.log_test_name('square')
        problem = ShortestPathProblem(self.nets.square, 4, 2)
        expected_solutions = [[(4, 1), (1, 2)],
                              [(4, 1), (1, 5), (5, 2)],
                              [(4, 5), (5, 2)]]
        self.check_answers(self.enumerator(problem, 3).get_solution_generator(), iter(expected_solutions))

    def test_diamonds(self):
        self.log_test_name('diamonds')
        problem = ShortestPathProblem(self.nets.diamonds, 1, 4)
        expected_solutions = [[(1, 6), (6, 4)],
                              [(1, 6), (6, 5), (5, 4)],
                              [(1, 6), (6, 3), (3, 4)],
                              [(1, 2), (2, 6), (6, 4)],
                              [(1, 2), (2, 6), (6, 3), (3, 4)],
                              [(1, 2), (2, 6), (6, 5), (5, 4)]]
        self.check_answers(self.enumerator(problem, 6).get_solution_generator(), iter(expected_solutions))


if __name__ == '__main__':
    unittest.main()
