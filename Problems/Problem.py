from abc import ABC, abstractmethod
from Problems.Solution import Solution


class Problem(ABC):

    @abstractmethod
    def solve(self, include_constrains: set, exclude_constraints: set) -> Solution:
        pass

    @abstractmethod
    def apply_penalty(self, occurrences: dict):
        pass
