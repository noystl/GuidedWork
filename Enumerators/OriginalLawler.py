from Enumerators.Enumerator import Enumerator
from heapq import *


class OriginalLawler(Enumerator):
    """
    Enumerates solutions according to Lawler's Algorithm.
    """
    def get_solution_generator(self):
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element[0]
            self.insert_new_solutions(top_element[0])

