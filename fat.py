import sys


class Fat(object):
    def __init__(self):
        self.fat = [-1] * 24985

    def set(self, index, value):
        if type(index) is not int:
            raise TypeError('type index is not int')
        if type(value) is not int:
            raise TypeError('type value is not int')
        if -1 > value or value > 24984:
            raise RuntimeError('valor deve estar entre 0 e 24984')
        self.fat[index] = value

    def get(self, index):
        if type(index) is not int:
            raise TypeError('type index is not int')
        return self.fat[index]

    def load(self, unidade):
        unidade.seek(3124)
        self.fat = [int.from_bytes(unidade.read(2), sys.byteorder, signed=True) for _ in range(0, 49970, 2)]

    def save(self, unidade):
        data = b''
        for value in self.fat:
            data += value.to_bytes(2, sys.byteorder, signed=True)
        unidade.seek(3124)
        unidade.write(data)
