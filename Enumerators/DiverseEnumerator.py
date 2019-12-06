from Enumerators.Enumerator import Enumerator
from SolutionData import SolutionData
from heapq import *


class DiverseEnumerator(Enumerator):
    def __init__(self, problem):
        super().__init__(problem)
        self.occurrences_dict = {}

    def __update_occurrences(self, top_element: SolutionData):
        for member in top_element.solution:
            if member not in self.occurrences_dict:
                self.occurrences_dict[member] = 0
            self.occurrences_dict[member] += 1

    def __update_queue(self):
        updated_queue = []
        while self.queue:
            top: SolutionData = heappop(self.queue)
            heappush(updated_queue, (self.problem.solve(top.include_constraints, top.exclude_constraints),
                                     top.include_constraints, top.exclude_constraints))

    def get_solution_generator(self):
        while self.queue:
            curr_sol = heappop(self.queue)
            yield curr_sol
            self.__update_occurrences(curr_sol[0])
            self.problem.apply_penalty(self.occurrences_dict)
            self.__update_queue()
            self.insert_new_solutions(curr_sol)
