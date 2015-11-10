import sys


class Fat(object):
    def __init__(self):
        self.fat = [-1] * 24985
        self.file = None

    def set(self, index, value):
        if type(index) is not int:
            raise TypeError('type index is not int')
        if type(value) is not int:
            raise TypeError('type value is not int')
        if 0 > value or value > 24984:
            raise RuntimeError('valor deve estar entre 0 e 24984')
        self.fat[index] = value

    def get(self, index):
        if type(index) is not int:
            raise TypeError('type index is not int')
        return self.fat[index]

    def set_file(self, file):
        self.file = file

    def load(self):
        if self.file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        self.file.seek(4000)
        self.fat = [int.from_bytes(self.file.read(2), sys.byteorder, signed=True) for _ in range(24985)]

    def save(self):
        if self.file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        self.file.seek(4000)
        for value in self.fat:
            self.file.write(value.to_bytes(2, sys.byteorder, signed=True))
