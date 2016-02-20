import logging
from itertools import islice
import parser as conf

logger = logging.getLogger(__name__)


class Algorithm(object):
    def __init__(self, root, to_child):
        self._root, self._to_child = root, to_child

    def top_down(self):
        frtu_list = []
        backbone_nodes = self._build_backbone()
        for branch_root in backbone_nodes:
            branch_nodes = []
            while branch_root is not None and (branch_root in self._to_child):
                branch_nodes.append(branch_root)
                candidates = [candidate for candidate in self._to_child[branch_root]
                              if candidate in self._to_child and candidate not in backbone_nodes]
                branch_root = candidates[-1] if len(candidates) != 0 else None
            frtu_list += list(islice(branch_nodes, 1, None, conf.max_uncovered_smart_meters))
        return frtu_list

    def _build_backbone(self):
        backbone_nodes = []
        branch_root = self._root
        while branch_root is not None:
            if branch_root not in self._to_child:
                raise ValueError('Branch root {0} does not exist in the graph.'.format(branch_root))
            backbone_nodes.append(branch_root)
            next_branch_root = None
            for branch_candidate in self._to_child[branch_root]:
                next_branch_root = branch_candidate if self._is_on_back_bone(branch_candidate) else None
            branch_root = next_branch_root
        return backbone_nodes

    def _is_on_back_bone(self, candidate):
        if candidate not in self._to_child:
            return False
        return all([neighbor in self._to_child for neighbor in self._to_child[candidate]])