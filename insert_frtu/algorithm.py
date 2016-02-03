from itertools import chain, product

import parser as params

from partial_solution import PartialSolution


class Algorithm(object):
    def __init__(self, root, to_child, leaf_probability):
        self._root, self._to_child, self._leaf_probability = root, to_child, leaf_probability
        self._partial_solutions = {}

    def bottom_up(self):
        return self._bottom_up(self._root)

    def _bottom_up(self, node):
        if node not in self._to_child or not self._to_child[node]:
            if node not in self._leaf_probability:
                raise ValueError('Node %s is a leaf with no attacking probability.' % node)
            probability = self._leaf_probability[node]
            return [PartialSolution(number_uncovered_smart_meter=1,
                                    accumulative_probability=probability if hasattr(probability, '__iter__')
                                    else (probability, probability))]
        solutions = filter(lambda raw: raw.number_uncovered_smart_meter <= params.max_uncovered_smart_meters,
                           self._child_solutions(node))
        # add FRTU at the root to create new partial solutions
        solutions += [PartialSolution(accumulative_probability=(0, 0), frtu_list=chain(solution.frtu_list, [node]))
                      for solution in solutions]
        # filter inferior solutions
        return _filter_inferior(solutions)

    def _child_solutions(self, node):
        left_solutions = self._bottom_up(self._to_child[node][0]) if len(self._to_child[node]) >= 1 else []
        right_solutions = self._bottom_up(self._to_child[node][1]) if len(self._to_child[node]) >= 2 else []
        # merge partial solutions from left and right sub-trees
        if not left_solutions:
            return right_solutions
        elif not right_solutions:
            return left_solutions
        return [left + right for left, right in product(left_solutions, right_solutions)]


def _filter_inferior(solutions):
    solutions = sorted(filter(lambda solution: solution.is_valid(), solutions),
                       key=lambda solution: (solution.number_frtu,
                                             solution.number_uncovered_smart_meter,
                                             solution.mean_probability))
    filtered_solutions = []
    for candidate_index, candidate in enumerate(solutions):
        if not filter(lambda benchmark: candidate.is_inferior_to(benchmark), solutions[:candidate_index]):
            filtered_solutions.append(candidate)
    return filtered_solutions
