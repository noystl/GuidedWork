from abc import ABC, abstractmethod


class Enumerator(ABC):
    def __init__(self, problem):
        self.problem = problem
        super(Enumerator, self).__init__()

    @abstractmethod
    def get_solution_generator(self):
        pass
