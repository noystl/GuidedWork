class SolutionData:
    def __init__(self, solution, include_constraints, exclude_constraints):
        self.solution = solution
        self.include_constraints = include_constraints
        self.exclude_constraints = exclude_constraints

    def __le__(self, other):
        return self.solution <= other.solution

    def __lt__(self, other):
        return self.solution < other.solution

    def __ge__(self, other):
        return self.solution > other.solution

    def __gt__(self, other):
        return self.solution >= other.solution
