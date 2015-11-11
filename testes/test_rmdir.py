import os
import unittest

import ep3


class TestRmdir(unittest.TestCase):
    def setUp(self):
        ep3.mount('test')
        ep3.mkdir('/novo')

    def test_rmdir(self):
        ep3.rmdir('/novo')
        self.assertEqual(False, ep3.root.tem('novo'))

    def test_rmdir_not_found(self):
        ep3.rmdir('/novdafo')

    def tearDown(self):
        os.remove('test')


if __name__ == '__main__':
    unittest.main()
