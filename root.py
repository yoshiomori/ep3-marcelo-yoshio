from time import asctime

import sys


class Root(object):
    def __init__(self):
        self.nome = '/'
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.tabela = {}
        self.file = None

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        self.modify = asctime()
        self.access = asctime()
        self.nome = nome

    def set_file(self, file):
        self.file = file

    def add_entry(self, nome, index):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if type(index) is not int:
            raise TypeError('type index is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        if len(self.tabela) > 392:
            raise RuntimeError('Tabela excedeu tamanho máximo 392')
        self.access = asctime()
        self.tabela[nome] = index

    def del_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if len(self.tabela) > 392:
            raise RuntimeError('Tabela excedeu tamanho máximo 392')
        self.access = asctime()
        self.tabela.pop(nome)

    def get_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if len(self.tabela) > 392:
            raise RuntimeError('Tabela excedeu tamanho máximo 392')
        return self.tabela[nome]

    def is_full(self):
        return len(self.tabela) >= 392

    def tem(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        return nome in self.tabela.keys()

    def load(self):
        if self.file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        self.file.seek(56000)
        self.nome = self.file.read(8).replace(b'\x00', b'').decode()
        self.access = self.file.read(24).decode()
        self.modify = self.file.read(24).decode()
        self.create = self.file.read(24).decode()
        self.tabela = dict()
        for _ in range(392):
            nome = self.file.read(8).replace(b'\x00', b'').decode()
            index = int.from_bytes(self.file.read(2), sys.byteorder)
            if nome is not '':
                self.tabela[nome] = index

    def save(self):
        if self.file is None:
            raise RuntimeError('Não foi carregado o arquivo')
        self.file.seek(56000)
        self.file.write(self.nome.encode('unicode_escape').rjust(8, b'\x00'))
        self.file.write(self.access.encode('unicode_escape'))
        self.file.write(self.modify.encode('unicode_escape'))
        self.file.write(self.create.encode('unicode_escape'))
        for nome, index in self.tabela.items():
            self.file.write(nome.encode('unicode_escape').rjust(8, b'\x00'))
            self.file.write(index.to_bytes(2, sys.byteorder))
        self.file.write(b'\x00' * (60000 - self.file.tell()))
