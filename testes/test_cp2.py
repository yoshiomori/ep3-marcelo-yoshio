import os
import unittest
from dados import Dados


class TestCp1(unittest.TestCase):
    def test_arquivo(self):
        try:
            import ep3
            ep3.mount('test')
            file = open('arq', 'w')
            file.write('ok'*99940000)
            file.close()
            ep3.cp('arq', '/arq')
            index = ep3.root.get_entry('arq')
            dado = Dados(ep3.bitmap, ep3.fat, 'arquivo', index)
            dado.load(ep3.unidade)
            os.remove('test')
            os.remove('arq')
            self.assertTrue(False)
        except MemoryError:
            self.assertTrue(True)
            os.remove('test')
            os.remove('arq')


if __name__ == '__main__':
    unittest.main()
