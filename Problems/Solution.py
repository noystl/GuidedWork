from abc import ABC, abstractmethod


class Solution(ABC):

    @abstractmethod
    def score(self):
        pass

    def __le__(self, other):
        return self.score() <= other.score()

    def __lt__(self, other):
        return self.score() < other.score()

    def __ge__(self, other):
        return self.score() > other.score()

    def __gt__(self, other):
        return self.score() >= other.score()
