import unittest
from Tests import NaiveTest
from Enumerators.LazyEnumerator import LazyEnumerator


class TestDiversifiedShortestPaths(NaiveTest.TestDiversifiedShortestPaths):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.enumerator = LazyEnumerator


if __name__ == '__main__':
    unittest.main()
