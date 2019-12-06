from abc import abstractmethod
from SolutionData import SolutionData
from heapq import *


class Enumerator:

    def __init__(self, problem):
        self.problem = problem
        self.queue = []
        heappush(self.queue, SolutionData(problem.solve([], []), [], []))

    def insert_new_solutions(self, top_element: SolutionData):
        new_include = top_element.include_constraints
        unfixed = top_element.solution.get_unfixed_elements()
        prev = []
        for elem in unfixed:
            new_include = new_include + prev
            new_exclude = top_element.exclude_constraints + [elem]
            new_queue_elem = SolutionData(self.problem.solve(new_include, new_exclude), new_include, new_exclude)
            if new_queue_elem.solution:
                heappush(self.queue, new_queue_elem)
            prev = [elem]

    @abstractmethod
    def get_solution_generator(self):
        pass

