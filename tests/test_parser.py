import unittest

from parser import conf


class TestConfiguration(unittest.TestCase):
    def test_read_conf(self):
        assert conf['max_uncovered_smart_meters'] == 5


if __name__ == '__main__':
    unittest.main()
