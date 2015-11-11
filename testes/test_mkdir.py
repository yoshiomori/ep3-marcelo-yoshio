import os
import unittest

import ep3


class TestMkdir(unittest.TestCase):
    def setUp(self):
        ep3.mount('test')
        ep3.mkdir('/novodir')

    def test_mkdir(self):
        self.assertEqual(True, ep3.root.tem('novodir'))

    def test_mkdir_3(self):
        ep3.mkdir('/novodir/novodir/')
        ep3.mkdir('/novodir/novodir/novodir/')
        self.assertTrue(True)

    def test_mkdir_miss_dir(self):
        try:
            ep3.mkdir('/novodir/nnnnn/teste')
            self.assertFalse(True)
        except FileNotFoundError:
            self.assertTrue(True)

    def tearDown(self):
        os.remove('test')


if __name__ == '__main__':
    unittest.main()
