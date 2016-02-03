import unittest
from partial_solution import PartialSolution


class TestPartialSolution(unittest.TestCase):
    def test_no_param_init(self):
        self.compare_partial_solution(PartialSolution(), 0, (0, 1), ())

    def test_param_init(self):
        accumulative_probability = (0.2, 0.8)
        frtu_list = (1, 2, 3)
        number_uncovered_smart_meter = 1
        partial_solution = PartialSolution(number_uncovered_smart_meter, accumulative_probability, frtu_list)
        self.compare_partial_solution(partial_solution,
                                      number_uncovered_smart_meter,
                                      accumulative_probability,
                                      frtu_list)

    def test_add(self):
        probability_left = (0.2, 0.8)
        frtu_list_left = (1, 2, 3)
        number_uncovered_smart_meter_left = 1
        partial_solution_left = PartialSolution(number_uncovered_smart_meter_left, probability_left, frtu_list_left)

        probability_right = (0.5, 0.6)
        frtu_list_right = (4, 5)
        number_uncovered_smart_meter_right = 2
        partial_solution_right = PartialSolution(number_uncovered_smart_meter_right, probability_right, frtu_list_right)

        probability = (probability_left[0] + probability_right[0] - probability_left[0] * probability_right[0],
                       probability_left[1] + probability_right[1] - probability_left[1] * probability_right[1])
        frtu_list = tuple(list(frtu_list_left) + list(frtu_list_right))
        number_uncovered_smart_meter = number_uncovered_smart_meter_left + number_uncovered_smart_meter_right

        self.compare_partial_solution(partial_solution_left + partial_solution_right,
                                      number_uncovered_smart_meter,
                                      probability,
                                      frtu_list)

    def test_add_unacceptable_type(self):
        with self.assertRaises(TypeError):
            PartialSolution() + 'not acceptable'

    def compare_partial_solution(self, solution, number_uncovered_smart_meter, accumulative_probability, frtu_list):
        assert solution.frtu_list == frtu_list
        assert solution._accumulative_probability == accumulative_probability
        assert solution.number_uncovered_smart_meter == number_uncovered_smart_meter
        assert solution.number_frtu == len(frtu_list)

    def test_inferior(self):
        benchmark = PartialSolution(5, (0.5, 0.7), (1, 2, 3))
        not_inferior = PartialSolution(5, (0.5, 0.6), (1, 2, 3, 4))
        inferior = PartialSolution(6, (0.5, 0.7), (1, 2, 3, 4))

        assert not not_inferior.is_inferior_to(benchmark)
        assert inferior.is_inferior_to(benchmark)
