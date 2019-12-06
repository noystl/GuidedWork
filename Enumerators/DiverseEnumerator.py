from Enumerators.Enumerator import Enumerator
from Problems.SolutionData import SolutionData
from heapq import *


class DiverseEnumerator(Enumerator):

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

            occurrences_dict = {}
            for member in top_element.solution.values:
                if member not in occurrences_dict:
                    occurrences_dict[member] = 0
                occurrences_dict[member] += 1

            self.problem.apply_penalty(occurrences_dict)
            self.__update_queue()
            self.insert_new_solutions(top_element)
