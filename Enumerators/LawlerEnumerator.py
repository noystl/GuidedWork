from Enumerators.Enumerator import Enumerator
from Problems.ShortestPaths.Graph import Graph
from Problems.ShortestPaths.ShortestPathProblem import ShortestPathProblem
from heapq import *


class LawlerEnumerator(Enumerator):
    def __init__(self, problem):
        self.queue = []
        heappush(self.queue, (problem.solve([], []), [], []))
        super(LawlerEnumerator, self).__init__(problem)

    def get_solution_generator(self) -> tuple:
        while self.queue:
            next_sol = heappop(self.queue)
            sol = next_sol[0]
            yield next_sol
            new_include = next_sol[1]
            unfixed = sol.get_unfixed_elements()
            prev = []
            for elem in unfixed:
                new_include = new_include + prev
                new_exclude = next_sol[2] + [elem]
                new_solution = (self.problem.solve(new_include, new_exclude), new_include, new_exclude)
                if new_solution[0]:
                    heappush(self.queue, new_solution)
                prev = [elem]


if __name__ == '__main__':
    graph = Graph()
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
        graph.add_edge(*edge)

    c = LawlerEnumerator(ShortestPathProblem(graph, '1', '5'))
    for sol in c.get_solution_generator():
        pass
        print("solution: " + str(sol[0]) + " I: " + str(sol[1]) + " E: " + str(sol[2]) + " score: " + str(sol[0].score()))
