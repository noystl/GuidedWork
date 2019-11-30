from Problems.Solution import Solution


class Path(Solution):
    def __init__(self, values: list, weights: dict):   # TODO: it's a little ugly to pass on the weights like that.
        self.values = values
        self.weights = weights

    def score(self):
        score = 0
        if len(self.values) > 0:
            curr_idx = 0
            next_idx = 1
            while next_idx < len(self.values):
                score += self.weights[(self.values[curr_idx], self.values[next_idx])]
                curr_idx = next_idx
                next_idx += 1

        return -score

    def __str__(self):
        return str(self.values)
