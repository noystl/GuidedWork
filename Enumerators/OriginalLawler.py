from Enumerators.Enumerator import Enumerator
from heapq import *


class OriginalLawler(Enumerator):

    def get_solution_generator(self):
        while self.queue:
            top_element = heappop(self.queue)
            yield top_element
            self.insert_new_solutions(top_element)

