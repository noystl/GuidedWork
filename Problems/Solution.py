from abc import abstractmethod


class Solution:
    """
    Represents a solution of an optimization problem.
    """

    def __init__(self, values):
        self.__unfixed_elements = []        # Elements that weren't added to this solution because of constraints.
        self.values = values                # The elements consisting this solution.
        self.current_cost = 0               # The current cost of this solution, penalty included.
        self.original_cost = 0              # The original cost of the solution, no penalty.

    @abstractmethod
    def get_original_cost(self) -> float:
        pass

    @abstractmethod
    def get_updated_cost(self) -> float:
        pass

    @abstractmethod
    def get_updated_values(self) -> set:
        """
        gets the elements in this solution who's cost was updated since the last time current_cost was updated.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Updates the score of this solution.
        """
        pass

    def set_unfixed_elements(self, unfixed: list):
        self.__unfixed_elements = unfixed

    def get_unfixed_elements(self) -> list:
        return self.__unfixed_elements

    def __lt__(self, other):
        return self.current_cost < other.current_cost

    def __ge__(self, other):
        return self.current_cost > other.current_cost

    def __eq__(self, other):
        return self.current_cost == other.current_cost
