from Enumerators.Enumerator import Enumerator
from Problems.Solution import Solution
from Problems.SolutionData import SolutionData
from heapq import *


class DiverseEnumerator(Enumerator):
    def __init__(self, problem):
        super().__init__(problem)
        self.occurrences_dict = {}

    def __update_occurrences(self, top_solution: Solution):
        for member in top_solution.values:
            if member not in self.occurrences_dict:
                self.occurrences_dict[member] = 0
            self.occurrences_dict[member] += 1

    def __update_queue(self):
        updated_queue = []
        while self.queue:
            top: SolutionData = heappop(self.queue)
            heappush(updated_queue, self.problem.solve(top.include_constraints, top.exclude_constraints))
        self.queue = updated_queue

    def get_solution_generator(self):
        while self.queue:
            top_element = heappop(self.queue)
            yield top_element
            self.__update_occurrences(top_element.solution)
            self.problem.apply_penalty(self.occurrences_dict)
            self.__update_queue()
            self.insert_new_solutions(top_element)
