import sys


class BitMap(object):
    def __init__(self):
        self.bitmap = int.from_bytes(b'\xff' * 3124, sys.byteorder)

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

    def parse_load(self, dado):
        self.bitmap = int.from_bytes(dado[0:3124], sys.byteorder)

    def save_format(self):
        return self.bitmap.to_bytes(3124, sys.byteorder)
