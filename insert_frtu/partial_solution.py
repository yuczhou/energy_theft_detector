from itertools import chain

import parser as params


class PartialSolution(object):
    def __init__(self, number_uncovered_smart_meter=0, accumulative_probability=(0, 1), frtu_list=()):
        self._accumulative_probability = tuple(accumulative_probability)
        self._number_uncovered_smart_meter = number_uncovered_smart_meter
        self._frtu_list = tuple(frtu_list)

    @property
    def frtu_list(self):
        return self._frtu_list

    @property
    def mean_probability(self):
        return sum(self._accumulative_probability) / len(self._accumulative_probability)

    @property
    def probability_range(self):
        return self._accumulative_probability

    @property
    def number_frtu(self):
        return len(self._frtu_list)

    @property
    def number_uncovered_smart_meter(self):
        return self._number_uncovered_smart_meter

    def is_valid(self):
        return self.number_uncovered_smart_meter <= params.max_uncovered_smart_meters \
               and self.mean_probability <= params.max_accumulative_probability

    def is_inferior_to(self, other):
        return other.number_frtu <= self.number_frtu \
               and other.number_uncovered_smart_meter <= self.number_uncovered_smart_meter \
               and other.mean_probability <= self.mean_probability

    def __eq__(self, other):
        return self.probability_range == other.probability_range \
               and self.number_uncovered_smart_meter == other.number_uncovered_smart_meter \
               and sorted(self.frtu_list) == sorted(other.frtu_list)

    def __add__(self, other):
        if type(other) is not PartialSolution:
            raise TypeError
        number_uncovered_smart_meter = self.number_uncovered_smart_meter + other.number_uncovered_smart_meter
        accumulative_probability = [left + right - left * right for left, right in
                                    zip(self.probability_range, other.probability_range)]
        frtu_list = chain(self.frtu_list, other.frtu_list)
        return PartialSolution(number_uncovered_smart_meter, accumulative_probability, frtu_list)

    def __str__(self):
        return 'Uncovered Smart Meter:%s, Accumulative Probability:%s, FRTUs:%s' \
               % (self._number_uncovered_smart_meter, self._accumulative_probability, self._frtu_list)
