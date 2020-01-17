from Enumerators.Enumerator import Enumerator
from Problems.SolutionData import SolutionData
from heapq import *


class LazyDiverseLawler(Enumerator):

    def __init__(self, problem, to_generate: int):
        super().__init__(problem, to_generate)
        if self.queue:
            self.optimal_score = self.queue[0].solution.current_score

    def insert_new_solutions(self, top_element: SolutionData):
        new_include = top_element.include_constraints
        unfixed = top_element.solution.get_unfixed_elements()
        prev = []
        for elem in unfixed:
            new_include = new_include + prev
            new_exclude = top_element.exclude_constraints + [elem]
            new_queue_elem = self.problem.solve(new_include, new_exclude)
            self.number_of_problems_solved += 1
            # if new_queue_elem:
            if new_queue_elem and new_queue_elem.solution.original_score <= 2 * self.optimal_score:
                heappush(self.queue, new_queue_elem)
            prev = [elem]

    def __update_queue(self):
        if self.queue:
            top = self.queue[0]
            while top.solution.current_score != top.solution.get_updated_score():
                heappop(self.queue)
                if top.solution.get_updated_values().issubset(set(top.include_constraints)):    # Todo: check this.
                    print('opt')
                    top.solution.update()
                    heappush(self.queue, top)
                else:
                    updated_sol_data = self.problem.solve(top.include_constraints, top.exclude_constraints)
                    # if updated_sol_data:
                    if updated_sol_data and updated_sol_data.solution.original_score <= 2 * self.optimal_score:
                        heappush(self.queue, updated_sol_data)
                    self.number_of_problems_solved += 1
                top = self.queue[0]

    def get_solution_generator(self):
        while self.queue and self.generated < self.to_generate:
            top_element = heappop(self.queue)
            self.generated += 1
            yield top_element

            self.problem.apply_penalty(top_element.solution.values)
            self.__update_queue()
            self.insert_new_solutions(top_element)
