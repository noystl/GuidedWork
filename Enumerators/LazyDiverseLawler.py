from Enumerators.Enumerator import Enumerator
from heapq import *


class LazyDiverseLawler(Enumerator):

    def __update_queue(self):       # Todo: find a more efficient way to calculate the updated score.
        if self.queue:
            next_top = self.queue[0]
            updated_top = self.problem.solve(next_top.include_constraints, next_top.exclude_constraints)
            while next_top.solution.updated_score() != updated_top.solution.updated_score():
                heappop(self.queue)
                heappush(self.queue, updated_top)
                next_top = self.queue[0]
                updated_top = self.problem.solve(next_top.include_constraints, next_top.exclude_constraints)

    def get_solution_generator(self):
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element

            occurrences_dict = {}
            for member in top_element.solution.values:
                if member not in occurrences_dict:
                    occurrences_dict[member] = 0
                occurrences_dict[member] += 1

            self.problem.apply_penalty(occurrences_dict)
            self.__update_queue()
            self.insert_new_solutions(top_element)
