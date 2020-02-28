from Enumerators.Enumerator import Enumerator
from abc import abstractmethod
from heapq import *


class DiverseEnumerator(Enumerator):
    """
    Enumerates solutions with regard to their diversity.
    """

    @abstractmethod
    def update_queue(self):
        """
        Updates the priority queue in order to make the queue invariant hold again.
        """
        pass

    def get_solution_generator(self):
        """
        A generator that yields solutions in ranked order, while taking into account their diversity.
        :return: a generator as described above.
        """
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element[0]

            self.problem.apply_penalty(top_element[0].solution.values)
            self.update_queue()
            self.insert_new_solutions(top_element[0])
