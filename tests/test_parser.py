import tempfile
import unittest

import parser as conf
from parser import read_tree_file


class TestConfiguration(unittest.TestCase):
    def test_read_conf(self):
        assert conf.max_uncovered_smart_meters == 5


class TestReadGraph(unittest.TestCase):
    def setUp(self):
        self._file = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self._file.close()

    def test_read_graph(self):
        self._file.writelines(['1 2\n', '1 3\n', '2 4\n'])
        self._file.seek(0)

        to_children, to_parent = read_tree_file(self._file.name)
        assert to_parent == {2:1, 3:1, 4:2}
        assert 1 in to_children
        assert to_children[1] == {2, 3}
        assert 2 in to_children
        assert to_children[2] == {4}

    def test_cylic_tree(self):
        self._file.writelines(['1 2\n', '1 3\n', '2 3\n'])
        self._file.seek(0)
        with self.assertRaises(ValueError):
            read_tree_file(self._file.name)

    def test_forest(self):
        self._file.writelines(['1 2\n', '3 4\n', '4 5\n'])
        self._file.seek(0)
        with self.assertRaises(ValueError):
            read_tree_file(self._file.name)

    def test_multiple_parents(self):
        self._file.writelines(['1 2\n', '1 3\n', '2 4\n', '3 4\n'])
        self._file.seek(0)
        with self.assertRaises(ValueError):
            read_tree_file(self._file.name)


if __name__ == '__main__':
    unittest.main()
