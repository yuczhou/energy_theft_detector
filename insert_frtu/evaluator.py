import random
import logging
from itertools import groupby

_MONTE_CARLO_SAMPLE_SIZE = 1000

logger = logging.getLogger(__name__)


class SolutionEvaluator(object):
    def __init__(self, to_parent, leaf_probability):
        self._leaf_probability = leaf_probability
        self._to_parent = to_parent

    def evaluate(self, frtu_list, sample_size=_MONTE_CARLO_SAMPLE_SIZE):
        if sample_size < 0:
            raise ValueError('Invalid sample size: {}.'.format(sample_size))
        frtu_map, leaf_to_frtu = self._build_frtu_map(frtu_list, self._leaf_probability.keys(), self._to_parent)
        cases = []
        for each_case in xrange(sample_size):
            fixed_leaf_probabilities = {leaf: random.uniform(*probability_range)
                                        for leaf, probability_range in self._leaf_probability.iteritems()}
            attacked_leaves = [leaf for leaf in fixed_leaf_probabilities.iterkeys()
                               if random.uniform(0, 1) <= fixed_leaf_probabilities[leaf]]
            if len(attacked_leaves) != 0:
                covered_leaves_for_frtu = [frtu_map[leaf_to_frtu[leaf]] for leaf in attacked_leaves]
                cases.append(sum(covered_leaves_for_frtu) / float(len(attacked_leaves)))
        average_meters_to_check = sum(cases) / float(len(cases)) if len(cases) != 0 else -1
        logger.info('Optimal solution with {0} FRTUs: {1}. Avg. smart meters to check: {2}'
                    .format(len(frtu_list), frtu_list, average_meters_to_check))
        return average_meters_to_check

    @staticmethod
    def _build_frtu_map(frtu_list, leaf_list, to_parent):
        frtu_map = {}
        leaf_to_frtu = {}
        for leaf in leaf_list:
            node = leaf
            while node not in frtu_list and node in to_parent:
                node = to_parent[node]
            frtu_map[node] = 1 if node not in frtu_map else frtu_map[node] + 1
            leaf_to_frtu[leaf] = node
        return frtu_map, leaf_to_frtu
