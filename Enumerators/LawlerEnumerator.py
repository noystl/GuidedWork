from Enumerators.Enumerator import Enumerator
from Problems.Problem import Problem
from heapq import *


class LawlerEnumerator(Enumerator):
    def __init__(self, problem):
        self.queue = []
        include = set()
        exclude = set()
        heappush(self.queue, problem.solve(include, exclude, 0))
        super(LawlerEnumerator, self).__init__(problem)

    def get_solution_generator(self) -> set:
        i = 1
        while self.queue:
            next_sol = heappop(self.queue)
            sol = next_sol[0][1]
            yield sol
            I = next_sol[1]
            E = next_sol[2]
            unfixed = sol.difference(I.union(E))
            prev = set()
            for elem in unfixed:
                set_elem = {elem}
                new_solution = self.problem.solve(I.union(prev), E.union(set_elem), i)
                heappush(self.queue, new_solution)
                prev = set_elem
            i += 1


if __name__ == '__main__':
    c = LawlerEnumerator(Problem(set()))
    print([*c.get_solution_generator()])
