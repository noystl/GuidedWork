import unittest
from Tests import OriginalLawlerTest
from Enumerators.NaiveEnumerator import NaiveEnumerator
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem


class TestDiversifiedShortestPaths(OriginalLawlerTest.TestShortestPath):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.enumerator = NaiveEnumerator

    def test_square(self, expected_solutions=None):     # TODO: Think how to avoid this code duplication.
        self.log_test_name('square')
        problem = ShortestPathProblem(self.nets.square, 4, 2)
        expected_solutions = [[(4, 1), (1, 2)],
                              [(4, 5), (5, 2)],
                              [(4, 1), (1, 5), (5, 2)]]
        self.check_answers(self.enumerator(problem, 3).get_solution_generator(), iter(expected_solutions))


if __name__ == '__main__':
    unittest.main()
