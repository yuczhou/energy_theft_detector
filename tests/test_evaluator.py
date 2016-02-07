import unittest

from evaluator import SingleSolutionEvaluator


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self._to_parent = {1: 0, 2: 0, 3: 1, 5: 3, 6: 3, 7: 1, 4: 2, 8: 4, 9: 4, 10: 2}
        self._leaf_probability = {leaf: [0.5, 0.6] for leaf in [5, 6, 7, 8, 9, 10]}

    def test_build_frtu_map(self):
        frtu_list = [1, 2]
        evaluator = SingleSolutionEvaluator(self._to_parent, self._leaf_probability, frtu_list)

        assert evaluator._frtu_map == {1:3, 2:3}
        assert evaluator._leaf_to_frtu == {5: 1, 6: 1, 7: 1, 8: 2, 9: 2, 10: 2}

    def test_evaluator_happy_path(self):
        frtu_list = [1, 2]
        evaluator = SingleSolutionEvaluator(self._to_parent, self._leaf_probability, frtu_list)
        assert evaluator.evaluate(10) == 3.0

    def test_evaluator_no_root_frtu(self):
        frtu_list = [1]
        evaluator = SingleSolutionEvaluator(self._to_parent, self._leaf_probability, frtu_list)
        assert evaluator.evaluate(10) == 3.0


if __name__ == '__main__':
    unittest.main()
