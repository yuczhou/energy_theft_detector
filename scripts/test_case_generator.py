import getopt
import random

import sys

_BRANCH_LEAVES_RANGE = (18, 24)
_PROBABILITY_RANGES = [(0.0, 0.1)] * 4 + [(0.5, 0.6)]
_TOTAL_LEAVES = 1000
_DELIMITER = '_'


def _create_branch(number_leaves):
    if number_leaves <= 0:
        raise ValueError('number of leaves cannot be {0}'.format(number_leaves))
    final_branch = {}
    leaves = {'l%db' % leaf: 'l%d' % leaf for leaf in xrange(1, number_leaves + 1)}
    branches = {'l%db' % (leaf - 1): 'l%db' % leaf for leaf in xrange(2, number_leaves + 1)}
    for source, sink in leaves.items() + branches.items():
        final_branch.setdefault(source, []).append(sink)
    final_branch['l0b'] = ['l1b']
    return 'l0b', final_branch


def _add_prefix_to_dict(prefix, org_dict):
    return {prefix + key: [prefix + value for value in values] for key, values in org_dict.items()}


def _create_floor(total_leaves):
    branch_leaf_numbers = []
    remains = total_leaves
    while remains > 0:
        branch_leaves = min(remains, random.randint(*_BRANCH_LEAVES_RANGE))
        branch_leaf_numbers.append(branch_leaves)
        remains -= branch_leaves
    branches = [(_create_branch(leaf_number)) for leaf_number in branch_leaf_numbers]
    return _merge_branches('b', branches)


def _merge_branches(prefix, branches):
    all_root, all_map = branches.pop(0)
    all_root = prefix + '0' + _DELIMITER + all_root
    all_map = _add_prefix_to_dict(prefix + '0' + _DELIMITER, all_map)
    branch_iter = 1
    for root_other, branch_other in branches:
        root_other = prefix + str(branch_iter) + _DELIMITER + root_other
        branch_other = _add_prefix_to_dict(prefix + str(branch_iter) + _DELIMITER, branch_other)
        all_map.update(branch_other)
        all_map[root_other].append(all_root)
        all_root = root_other
        branch_iter += 1
    return all_root, all_map


def _get_leaves(building_root, building_map):
    leaves = []
    q = [building_root]
    while len(q) != 0:
        node = q.pop()
        if node not in building_map or len(building_map[node]) == 0:
            leaves.append(node)
            continue
        for neighbor in building_map[node]:
            q.append(neighbor)
    return leaves


def _write_structure_file(file_name, building_map):
    with open(file_name, 'w') as f:
        for source, sinks in building_map.iteritems():
            map(lambda sink: f.write('%s %s\n' % (source, sink)), sinks)


def _write_probability_file(file_name, leaves):
    with open(file_name, 'w') as f:
        for leaf in leaves:
            p_low, p_high = _PROBABILITY_RANGES[random.randint(0, len(_PROBABILITY_RANGES) - 1)]
            f.write('%s %f %f\n' % (leaf, p_low, p_high))


def _main(argv):
    try:
        opts, args = getopt.getopt(argv, "s:p:", ["structure=", "probability="])
    except getopt.GetoptError:
        print 'insert_frtu.py -s <structure file> -p <probability file>'

    tree_structure_file, probability_file = ('structure.txt', 'probability.txt')
    for opt, arg in opts:
        if opt in ("-s", "--structure"):
            tree_structure_file = arg
        elif opt in ("-p", "--probability"):
            probability_file = arg
    random.seed(0)
    building_root, building_map = _create_floor(_TOTAL_LEAVES)
    _write_probability_file(probability_file, _get_leaves(building_root, building_map))
    _write_structure_file(tree_structure_file, building_map)


if __name__ == '__main__':
    _main(sys.argv[1:])
