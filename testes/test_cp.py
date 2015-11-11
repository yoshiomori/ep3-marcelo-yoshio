import os
import unittest

import ep3
from dados import Dados


class TestCp(unittest.TestCase):
    def setUp(self):
        ep3.mount('test')
        file = open('arq', 'w')
        file.write('ok')
        file.close()
        ep3.cp('arq', '/arq')

    def test_cp(self):
        self.assertEqual(ep3.root.tem('arq'), True)

    def test_arquivo(self):
        index = ep3.root.get_entry('arq')
        dado = Dados(ep3.bitmap, ep3.fat, 'arquivo', index)
        dado.load(ep3.unidade)
        self.assertEqual(dado.arquivo.dado, 'ok')

    def tearDown(self):
        os.remove('test')
        os.remove('arq')


if __name__ == '__main__':
    unittest.main()
