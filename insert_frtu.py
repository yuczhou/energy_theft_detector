import getopt
import logging

import os
import sys

import insert_frtu.parser as parser
import insert_frtu.algorithm as algorithm
from insert_frtu.evaluator import SolutionEvaluator

# log to console for simplicity
logging.basicConfig(level=logging.DEBUG)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "s:p:", ["structure=", "probability="])
    except getopt.GetoptError:
        print 'insert_frtu.py -s <structure file> -p <probability file>'

    tree_structure_file, probability_file = ('', '')
    for opt, arg in opts:
        if opt in ("-s", "--structure"):
            tree_structure_file = arg
        elif opt in ("-p", "--probability"):
            probability_file = arg
    if not os.path.isfile(tree_structure_file):
        raise 'Tree structure file {0} does not exist'.format(tree_structure_file)
    if not os.path.isfile(probability_file):
        raise 'Probability file {0} does not exist'.format(probability_file)

    root, to_child, to_parent = parser.read_tree_file(tree_structure_file)
    leaf_probability = parser.read_probability_file(probability_file)
    solutions = algorithm.Algorithm(root, to_child).top_down()
    SolutionEvaluator(to_parent, leaf_probability).evaluate(solutions)


if __name__ == '__main__':
    main(sys.argv[1:])
