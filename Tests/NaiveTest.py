import unittest
from Tests import LawlerTest
from Enumerators.NaiveEnumerator import NaiveEnumerator
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem


class TestDiversifiedShortestPaths(LawlerTest.TestShortestPath):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.enumerator = NaiveEnumerator

    def test_square(self, expected_solutions=None):
        self.log_test_name('square')
        problem = ShortestPathProblem(self.nets.square, 4, 2, lambda x: x + 3)
        expected_solutions = [[(4, 1), (1, 2)],
                              [(4, 5), (5, 2)],
                              [(4, 1), (1, 5), (5, 2)]]
        self.check_answers(self.enumerator(problem, 3).get_solution_generator(), iter(expected_solutions))

    def test_diamonds(self):
        self.log_test_name('diamonds')
        problem = ShortestPathProblem(self.nets.diamonds, 1, 4, lambda x: x + 2)
        expected_solutions = [[(1, 6), (6, 4)],
                              [(1, 2), (2, 6), (6, 5), (5, 4)],
                              [(1, 6), (6, 3), (3, 4)],
                              [(1, 2), (2, 6), (6, 4)],
                              [(1, 6), (6, 5), (5, 4)],
                              [(1, 2), (2, 6), (6, 3), (3, 4)]]
        self.check_answers(self.enumerator(problem, 6).get_solution_generator(), iter(expected_solutions))


if __name__ == '__main__':
    unittest.main()
