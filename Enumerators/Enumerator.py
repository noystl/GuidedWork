from abc import abstractmethod
from Problems.SolutionData import SolutionData
from heapq import *


class Enumerator:

    def __init__(self, problem, to_generate: int):
        self.problem = problem
        self.to_generate = to_generate
        self.generated = 0
        self.queue = []
        sol_data = problem.solve([], [])
        if sol_data:
            heappush(self.queue, problem.solve([], []))

    def insert_new_solutions(self, top_element: SolutionData):
        new_include = top_element.include_constraints
        unfixed = top_element.solution.get_unfixed_elements()
        prev = []
        for elem in unfixed:
            new_include = new_include + prev
            new_exclude = top_element.exclude_constraints + [elem]
            new_queue_elem = self.problem.solve(new_include, new_exclude)
            if new_queue_elem:
                heappush(self.queue, new_queue_elem)
            prev = [elem]

    @abstractmethod
    def get_solution_generator(self):
        pass

