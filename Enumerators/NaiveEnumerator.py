from Enumerators.DiverseEnumerator import DiverseEnumerator
from heapq import *


class NaiveEnumerator(DiverseEnumerator):
    """
    Updates the queue in a naive fashion.
    """

    def update_queue(self):
        updated_queue = []
        while self.queue:
            top_data, top_tie_beaker = heappop(self.queue)
            updated_sol_data = self.problem.solve(top_data.include_constraints, top_data.exclude_constraints)
            heappush(updated_queue, (updated_sol_data, top_tie_beaker))
            self.number_of_problems_solved += 1
        self.queue = updated_queue
