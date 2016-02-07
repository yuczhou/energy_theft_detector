import random

_MONTE_CARLO_SAMPLE_SIZE = 1000


class SingleSolutionEvaluator(object):
    def __init__(self, to_parent, leaf_probability, frtu_list):
        self._leaf_probability = leaf_probability
        self._build_frtu_map(frtu_list, leaf_probability.keys(), to_parent)

    def evaluate(self, sample_size=_MONTE_CARLO_SAMPLE_SIZE):
        if sample_size < 0:
            raise ValueError('Invalid sample size: {}.'.format(sample_size))
        cases = []
        for each_case in range(sample_size):
            fixed_leaf_probabilities = {leaf: random.uniform(*probability_range)
                                        for leaf, probability_range in self._leaf_probability.iteritems()}
            attacked_leaves = [leaf for leaf in fixed_leaf_probabilities.iterkeys()
                               if random.uniform(0, 1) <= fixed_leaf_probabilities[leaf]]
            if len(attacked_leaves) != 0:
                covered_leaves_for_frtu = [self._frtu_map[self._leaf_to_frtu[leaf]] for leaf in attacked_leaves]
                cases.append(sum(covered_leaves_for_frtu) / float(len(attacked_leaves)))
        return sum(cases) / float(len(cases)) if len(cases) != 0 else -1

    def _build_frtu_map(self, frtu_list, leaf_list, to_parent):
        self._frtu_map = {}
        self._leaf_to_frtu = {}
        for leaf in leaf_list:
            node = leaf
            while node not in frtu_list and node in to_parent:
                node = to_parent[node]
            self._frtu_map[node] = 1 if node not in self._frtu_map else self._frtu_map[node] + 1
            self._leaf_to_frtu[leaf] = node
