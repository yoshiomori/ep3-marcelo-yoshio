from math import ceil

from arquivo import ArquivosRegulares, Directory
from fat import Fat
from mapa_bits import BitMap


class Dados(object):
    def __init__(self, bitmap=None, fat=None, tipo=None, index=-1):
        self.indexes = []
        self.last_index = index
        if tipo == 'diretorio':
            self.arquivo = Directory()
        elif tipo == 'arquivo':
            self.arquivo = ArquivosRegulares()
        elif tipo is None:
            self.arquivo = None
        else:
            raise RuntimeError('tipo diretorio, arquivo')
        self.bitmap = bitmap
        self.fat = fat

    def load(self, index, fat, file):
        file.seek(60000 + index * 4000)
        file.read(4000)

    def save(self, file):
        if self.arquivo is not None:
            dado = self.arquivo.save_format()
            if self.last_index == -1:
                for index in range(24985):
                    if self.bitmap.get(index):
                        self.last_index = index
            if len(self.indexes) < ceil(len(dado) / 4000):
                for index in range(24985):
                    if self.bitmap.get(index):
                        self.bitmap.set_0(index)
                        self.fat[self.last_index] = index
                        self.indexes.append(self.last_index)
                        self.last_index = index
                        if len(self.indexes) < ceil(len(dado) / 4000):
                            self.fat[self.last_index] = -1
                            break
            while len(self.indexes) > ceil(len(dado) / 4000):
                self.bitmap.set_1(self.last_index)
                self.last_index = self.indexes.pop()
                self.fat[self.last_index] = -1
            for index in self.indexes:
                start = index * 4000
                file.seek(60000+start)
                file.write(dado[start:start+4000])
            start = self.last_index * 4000
            file.seek(60000+start)
            file.write(dado[start:])
        else:
            file.seek(60000)
            file.write(b'\x00' * 99940000)
