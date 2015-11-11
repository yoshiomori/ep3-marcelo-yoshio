import os
import unittest

import ep3


class TestMount(unittest.TestCase):
    def setUp(self):
        ep3.mount('test')
        self.bitmap = ep3.bitmap
        self.fat = ep3.fat.fat
        self.root = ep3.root

    def test_mount_bitmap(self):
        ep3.mount('test')
        self.assertEqual(self.bitmap, ep3.bitmap)

    def test_mount_fat(self):
        ep3.mount('test')
        self.assertListEqual(self.fat, ep3.fat.fat)

    def test_mount_root(self):
        ep3.mount('test')
        self.assertEqual(self.root.nome, ep3.root.nome)
        self.assertEqual(self.root.access, ep3.root.access)
        self.assertEqual(self.root.modify, ep3.root.modify)
        self.assertEqual(self.root.create, ep3.root.create)
        self.assertDictEqual(self.root.tabela, ep3.root.tabela)

    def tearDown(self):
        os.remove('test')


if __name__ == '__main__':
    unittest.main()
