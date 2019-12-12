from abc import abstractmethod


class Solution:
    def __init__(self, values):
        self.__unfixed_elements = []
        self.values = values

    @abstractmethod
    def original_score(self) -> float:
        pass

    @abstractmethod
    def updated_score(self) -> float:
        pass

    def set_unfixed_elements(self, unfixed: list):
        self.__unfixed_elements = unfixed

    def get_unfixed_elements(self) -> list:
        return self.__unfixed_elements

    def __le__(self, other):
        return self.updated_score() <= other.updated_score()     # todo: maybe score should be an attribute of solution

    def __lt__(self, other):
        return self.updated_score() < other.updated_score()

    def __ge__(self, other):
        return self.updated_score() > other.updated_score()

    def __gt__(self, other):
        return self.updated_score() >= other.updated_score()
