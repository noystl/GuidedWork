
from Problems.Solution import Solution


class Path(Solution):
    def __init__(self, values: list, weights: dict):   # TODO: it's a little ugly to pass on the weights like that.
        super().__init__(values)
        self.weights = weights

    def score(self):
        score = 0
        for edge in self.values:
            score += self.weights[edge]
        return score

    def __str__(self):
        return str(self.values)
