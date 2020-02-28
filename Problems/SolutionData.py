class SolutionData:
    """
    An object that contains a solution with additional data.
    """

    def __init__(self, solution, include_constraints, exclude_constraints):
        self.solution = solution
        self.include_constraints = include_constraints      # Defines what elements this solution must contain.
        self.exclude_constraints = exclude_constraints      # Defines what elements this solution must not contain.

    def __lt__(self, other):
        return self.solution < other.solution

    def __ge__(self, other):
        return self.solution > other.solution

    def __eq__(self, other):
        return self.solution == other.solution
