import sys


class BitMap(object):
    def __init__(self):
        self.bitmap = int.from_bytes(b'\xff' * 3124, sys.byteorder)
        self.file = None

    def set_0(self, index):
        if type(index) is not int:
            raise TypeError('type índex is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        self.bitmap &= ~(1 << index)

    def set_1(self, index):
        if type(index) is not int:
            raise TypeError('type índex is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        self.bitmap |= 1 << index

    def get(self, index):
        if type(index) is not int:
            raise TypeError('type índex is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        return self.bitmap >> index & 1

    def set_file(self, file):
        self.file = file

    def load(self):
        if self.file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        self.file.seek(0)
        self.bitmap = int.from_bytes(self.file.read(3124), sys.byteorder)

    def save(self):
        if self.file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        self.file.seek(0)
        self.file.write(self.bitmap.to_bytes(3124, sys.byteorder))
