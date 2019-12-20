from Enumerators.Enumerator import Enumerator
from heapq import *


class LazyDiverseLawler(Enumerator):

    def __update_queue(self):
        if self.queue:
            top = self.queue[0]
            while top.solution.current_score != top.solution.get_updated_score():
                heappop(self.queue)
                if top.solution.get_updated_values().issubset(set(top.include_constraints)):    # Todo: check this.
                    print("Noy")
                    heappush(self.queue, top.solution.update())
                else:
                    heappush(self.queue, self.problem.solve(top.include_constraints, top.exclude_constraints))
                top = self.queue[0]

    def get_solution_generator(self):
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element

            self.problem.apply_penalty(top_element.solution.values)
            self.__update_queue()
            self.insert_new_solutions(top_element)
