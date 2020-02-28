from Enumerators.DiverseEnumerator import DiverseEnumerator
from heapq import *


class LazyEnumerator(DiverseEnumerator):
    """
    Updates the queue in a lazy fashion.
    """

    def update_queue(self):
        if self.queue:
            top_data, top_tie_breaker = self.queue[0]
            while top_data.solution.current_cost != top_data.solution.get_updated_cost():
                heappop(self.queue)
                if top_data.solution.get_updated_values().issubset(set(top_data.include_constraints)):
                    top_data.solution.update()
                    heappush(self.queue, (top_data, top_tie_breaker))
                else:
                    updated_sol_data = self.problem.solve(top_data.include_constraints, top_data.exclude_constraints)
                    heappush(self.queue, (updated_sol_data, top_tie_breaker))
                    self.number_of_problems_solved += 1
                top_data, top_tie_breaker = self.queue[0]
