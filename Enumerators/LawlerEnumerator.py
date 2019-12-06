from Enumerators.Enumerator import Enumerator
from heapq import *


class LawlerEnumerator(Enumerator):

    def get_solution_generator(self):
        while self.queue:
            curr_sol = heappop(self.queue)
            yield curr_sol
            self.insert_new_solutions(curr_sol)

