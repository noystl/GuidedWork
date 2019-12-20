import unittest
from Tests import DiverseLawlerTest
from Enumerators.LazyDiverseLawler import LazyDiverseLawler


class TestDiversifiedShortestPaths(DiverseLawlerTest.TestDiversifiedShortestPaths):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.enumerator = LazyDiverseLawler


if __name__ == '__main__':
    unittest.main()
