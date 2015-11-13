import os
import unittest

import ep3


class TestMkdir(unittest.TestCase):

    def test_mkdir(self):
        ep3.mount('test')
        ep3.mkdir('/novodir')
        self.assertEqual(True, ep3.root.tem('novodir'))
        ep3.mkdir('/novodir/novodir/')
        ep3.mkdir('/novodir/novodir/novodir/')
        self.assertTrue(True)
        try:
            ep3.mkdir('/novodir/nnnnn/teste')
            self.assertFalse(True)
        except FileNotFoundError:
            self.assertTrue(True)
        os.remove('test')

if __name__ == '__main__':
    unittest.main()
