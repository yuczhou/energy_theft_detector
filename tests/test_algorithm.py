import unittest
import algorithm
import parser as conf


class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        self.to_child = {1: [2, 8], 2: [3, 5], 3: [4, 6], 4: [7], 8: [9], 9: [10, 11], 10: [12]}
        self.algorithm = algorithm.Algorithm(1, self.to_child)

    def test_build_backbone(self):
        assert [1, 8] == self.algorithm._build_backbone()

    def test_top_down(self):
        conf.max_uncovered_smart_meters = 2
        assert [2, 4, 9] == self.algorithm.top_down()


if __name__ == '__main__':
    unittest.main()
