from abc import ABC, abstractmethod
from Problems.SolutionData import SolutionData


class Problem(ABC):
    """
    Represents a general optimization problem.
    """

    def __init__(self, penalty_func=lambda x: x):
        self.penalty_func = penalty_func

    @abstractmethod
    def solve(self, include_constrains: set, exclude_constraints: set) -> SolutionData:
        """
        Gets a solution for this problem, under constraints.
        :param include_constrains: defines what elements has to be in the solution.
        :param exclude_constraints: defines what elements mast not be in the solution.
        :return: a SolutionData object, containing the solution with some related data.
        """
        pass

    @abstractmethod
    def apply_penalty(self, to_penalize: list):
        """
        Increases the cost of the elements in to_penalize according to self.penalty_function.
        """
        pass
