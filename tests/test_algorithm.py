import unittest
import algorithm
from partial_solution import PartialSolution


class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        """
            ------0------
           /             \
           1             2
          / \           / \
          3 |           4 |
         /| |          /| |
        5 6 7         8 9 10
        """
        self.to_child = {0: [1, 2], 1: [3, 7], 3: [5, 6], 2: [4, 10], 4: [8, 9]}
        self.leaf_probability = {leaf: 0 for leaf in [5, 6, 7, 8, 9, 10]}
        self.algorithm = algorithm.Algorithm(0, self.to_child, self.leaf_probability)

    def test_filter_inferior(self):
        one_frtu = PartialSolution(5, (0.1, 0.2), (1,))
        one_frtu_inferior = PartialSolution(5, (0.1, 0.3), (1,))
        two_frtu = PartialSolution(3, (0.2, 0.3), (1, 2))
        two_frtu_inferior = PartialSolution(4, (0.2, 0.3), (1, 2))
        filtered_solutions = algorithm._filter_inferior([two_frtu_inferior, one_frtu_inferior, two_frtu, one_frtu])

        assert filtered_solutions == [one_frtu, two_frtu]

    def test_bottom_up_number_of_uncovered_leaves(self):
        # so it is supposed to add FRTU at 1, instead of 2
        self.leaf_probability[5] = 0.1
        solutions = self.algorithm.bottom_up()
        solutions = sorted(solutions, key=lambda solution: solution.number_frtu)

        assert len(solutions) == 2
        assert solutions[0] == PartialSolution(3, (0, 0), [1])
        assert solutions[1] == PartialSolution(0, (0, 0), [1, 2])

    def test_bottom_up_accumulative_probability(self):
        map(lambda key: self.leaf_probability.update({key: 0.5}), self.leaf_probability.keys())
        solutions = self.algorithm.bottom_up()

        assert len(solutions) == 1
        assert solutions[0] == PartialSolution(0, (0, 0), [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
