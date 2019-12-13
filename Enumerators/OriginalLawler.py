from Enumerators.Enumerator import Enumerator
from heapq import *


class OriginalLawler(Enumerator):

    def get_solution_generator(self):
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element
            self.insert_new_solutions(top_element)

