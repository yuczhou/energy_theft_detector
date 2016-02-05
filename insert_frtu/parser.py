from ConfigParser import SafeConfigParser

import re

_MAX_UNCOVERED_SMART_METER = 'max_uncovered_smart_meters'
_MAX_ACCUMULATIVE_PROBABILITY = 'max_accumulative_probability'

_MAX_TREE_BRANCHES = 2


def read_tree_file(file_name):
    graph = {}
    with open(file_name) as file:
        for line in file:
            if not re.match(r'\d+\s+\d+', line):
                continue
            source, sink = map(int, line.split())
            graph.setdefault(source, set()).add(sink)
    validate_tree(graph)
    return graph, to_parent(graph)


def to_parent(to_children):
    graph = {}
    for source, sinks in to_children.iteritems():
        graph.update({sink: source for sink in sinks})
    return graph


def validate_tree(graph):
    union_find = _UnionFind()
    visited = {}
    for source, sinks in graph.iteritems():
        if len(sinks) > _MAX_TREE_BRANCHES:
            raise ValueError('Node {0} has more than 2 children: {1}.'.format(source, sinks))
        for sink in sinks:
            if sink in visited:
                raise ValueError('{0} has more than 1 parents: {1}'.format(sink, [visited[sink], source]))
            visited[sink] = source
            if union_find[source] == union_find[sink]:
                raise ValueError('{0} and {1} should not be connected.'.format(source, sink))
            union_find.union(source, sink)
    roots = filter(lambda node: union_find[node] == node, union_find)
    if len(roots) is not 1:
        raise ValueError('Tree has multiple roots: {0}'.format(roots))

"""UnionFind.py

Union-find data structure. Based on Josiah Carlson's code,
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
with significant additional changes by D. Eppstein.
"""


class _UnionFind:
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r],r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def _build_conf():
    parser = SafeConfigParser()
    parser.read('resources/parameters.ini')
    typed_dict = {}

    param_type = 'ints'
    for name in parser.options(param_type):
        typed_dict[name] = parser.getint(param_type, name)
    param_type = 'floats'
    for name in parser.options(param_type):
        typed_dict[name] = parser.getfloat(param_type, name)

    return typed_dict


_conf = _build_conf()
max_uncovered_smart_meters = _conf[_MAX_UNCOVERED_SMART_METER]
max_accumulative_probability = _conf[_MAX_ACCUMULATIVE_PROBABILITY]

