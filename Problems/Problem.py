from abc import ABC, abstractmethod
from Problems.SolutionData import SolutionData


class Problem(ABC):

    @abstractmethod
    def solve(self, include_constrains: set, exclude_constraints: set) -> SolutionData:
        pass

    @abstractmethod
    def apply_penalty(self, occurrences: dict):
        pass
