from Problems.Solution import Solution


class Path(Solution):
    def __init__(self, values: list, original_weights: dict, updated_weights: dict):
        super().__init__(values)
        self.original_weights = original_weights
        self.updated_weights = updated_weights

    def original_score(self):
        score = 0
        for edge in self.values:
            score += self.original_weights[edge]
        return score

    def updated_score(self):
        score = 0
        for edge in self.values:
            score += self.updated_weights[edge]
        return score

    def __str__(self):
        return str(self.values)
