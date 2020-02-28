from abc import abstractmethod
from Problems.SolutionData import SolutionData
from heapq import *


class Enumerator:
    """
    Represents an object that when given a problem can output it's solutions in ranked order.
    """

    def __init__(self, problem, to_generate: int):
        self.problem = problem                          # An optimization problem
        self.to_generate = to_generate                  # The number of solutions to generate.
        self.generated = 0                              # Counts how many solutions where generated until now.
        self.queue = []                                 # Priority queue
        self.tie_breaker = 0                            # A deterministic tie breaker for the priority queue.
        self.number_of_problems_solved = 0
        sol_data = problem.solve([], [])                # Gets the first (optimal) solution, if exists.
        if sol_data:
            heappush(self.queue, (sol_data, self.tie_breaker))
            self.tie_breaker -= 1

    def insert_new_solutions(self, top_element: SolutionData):
        """
        Inserts into the queue the "descendants" of the solution produced in this iteration.
        :param top_element: the data of the solution produced in this iteration.
        """
        new_include = top_element.include_constraints
        unfixed = top_element.solution.get_unfixed_elements()
        prev = []
        for elem in unfixed:
            new_include = new_include + prev
            new_exclude = top_element.exclude_constraints + [elem]
            new_sol_data = self.problem.solve(new_include, new_exclude)
            self.number_of_problems_solved += 1
            if new_sol_data:
                heappush(self.queue, (new_sol_data, self.tie_breaker))
                self.tie_breaker -= 1
            prev = [elem]

    @abstractmethod
    def get_solution_generator(self):
        """
        Creates a generator of solutions. The generator outputs solutions to self.problem in ranked order.
        :return: the mentioned solution generator.
        """
        pass
