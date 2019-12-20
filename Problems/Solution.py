from abc import abstractmethod


class Solution:
    def __init__(self, values):
        self.__unfixed_elements = []
        self.values = values
        self.current_score = 0
        self.original_score = 0

    @abstractmethod
    def get_original_score(self) -> float:
        pass

    @abstractmethod
    def get_updated_score(self) -> float:
        pass

    def set_unfixed_elements(self, unfixed: list):
        self.__unfixed_elements = unfixed

    def get_unfixed_elements(self) -> list:
        return self.__unfixed_elements

    def __le__(self, other):
        return self.current_score <= other.current_score

    def __lt__(self, other):
        return self.current_score < other.current_score

    def __ge__(self, other):
        return self.current_score > other.current_score

    def __gt__(self, other):
        return self.current_score >= other.current_score
