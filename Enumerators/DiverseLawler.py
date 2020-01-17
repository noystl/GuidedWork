from Enumerators.Enumerator import Enumerator
from Problems.SolutionData import SolutionData
from heapq import *


class DiverseLawler(Enumerator):

    def __update_queue(self):
        updated_queue = []
        while self.queue:
            top: SolutionData = heappop(self.queue)
            heappush(updated_queue, self.problem.solve(top.include_constraints, top.exclude_constraints))
            self.number_of_problems_solved += 1
        self.queue = updated_queue

    def get_solution_generator(self):
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element

            self.problem.apply_penalty(top_element.solution.values)
            self.__update_queue()
            self.insert_new_solutions(top_element)
