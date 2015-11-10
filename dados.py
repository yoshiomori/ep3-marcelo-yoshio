from time import asctime

import sys


class ArquivosRegulares(object):
    def __init__(self):
        self.nome = ''
        self.tamanho = 0
        self.access = ''
        self.modify = ''
        self.create = ''
        self.dado = ''
        self.index = -1
        self.indexes = []

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if self.index == -1:
            raise RuntimeError('Arquivo não mapeado')
        self.access = asctime()
        self.modify = asctime()
        self.nome = nome

    def get_nome(self):
        if self.index == -1:
            raise RuntimeError('Arquivo não mapeado')
        return self.nome

    def set(self, nome, dado, indexes):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if type(dado) is not str:
            raise TypeError('type dado is not str')
        if type(indexes) is not list:
            raise TypeError('type indexes is not list')
        if indexes is []:
            raise RuntimeError('indexes is empty')
        for index in indexes:
            if index < 0 or 24984 < index:
                raise RuntimeError('Todas as entradas do index devem estar entre 0 e 24984')
        resto = (len(indexes) - 1) * 4000 + 3920 - len(dado)
        if 0 > resto or resto > 4000:
            raise RuntimeError('dado e indexes mal formado')
        self.nome = nome
        self.index = indexes.pop()
        self.indexes = indexes
        self.create = asctime()
        self.modify = asctime()
        self.access = asctime()
        self.dado = dado
        self.tamanho = len(dado)

    def set_dado(self, dado, indexes):
        if type(dado) is not str:
            raise TypeError('type dado is not str')
        if type(indexes) is not list:
            raise TypeError('type indexes is not list')
        if indexes is []:
            raise RuntimeError('indexes is empty')
        for index in indexes:
            if index < 0 or 24984 < index:
                raise RuntimeError('Todas as entradas do index devem estar entre 0 e 24984')
        resto = (len(indexes) - 1) * 4000 + 3920 - len(dado)
        if 0 > resto or resto > 4000:
            raise RuntimeError('dado e indexes mal formado')
        if self.index == -1:
            raise RuntimeError('Arquivo não mapeado')
        self.index = indexes.pop
        self.indexes = indexes
        self.modify = asctime()
        self.access = asctime()
        self.dado = dado
        self.tamanho = len(dado)

    def get_dado(self):
        if self.index == -1:
            raise RuntimeError('Arquivo não mapeado')
        self.access = asctime()
        return self.dado

    def load(self, file, indexes):
        if file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        if type(indexes) is not list:
            raise TypeError('type indexes is not list')
        if indexes is []:
            raise RuntimeError('indexes is empty')
        for index in indexes:
            if index < 0 or 24984 < index:
                raise RuntimeError('Todas as entradas do index devem estar entre 0 e 24984')
        self.index = indexes.pop(0)
        self.indexes = indexes
        file.seek(60000 + self.index * 4000)
        self.nome = file.read(8).replace(b'\x00', b'').decode()
        self.tamanho = int.from_bytes(file.read(4), sys.byteorder)
        self.create = file.read(24).decode()
        self.modify = file.read(24).decode()
        self.access = file.read(24).decode()
        dado = file.read(3916)
        for index in indexes:
            file.seek(60000 + index * 4000)
            dado += file.read(4000)
        self.dado = dado[:self.tamanho].decode()

    def save(self, file):
        if file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        if self.index == -1:
            raise RuntimeError('Arquivo não mapeado')
        file.seek(60000 + self.index * 4000)
        file.write(self.nome.encode('ascii', 'replace').rjust(8, b'\x00'))
        file.write(self.tamanho.to_bytes(4, sys.byteorder))
        file.write(self.create.encode('ascii', 'replace'))
        file.write(self.modify.encode('ascii', 'replace'))
        file.write(self.access.encode('ascii', 'replace'))
        start = 0
        stop = min(3916, self.tamanho)
        file.write(self.dado[start:stop].encode('ascii', 'replace'))
        for index in self.indexes:
            start, stop = stop, min(4000 + stop, self.tamanho)
            file.seek(60000 + index * 4000)
            file.write(self.dado[start:stop].encode('ascii', 'replace'))
