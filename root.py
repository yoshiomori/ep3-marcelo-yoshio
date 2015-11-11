from time import asctime

import sys


class Root(object):
    def __init__(self):
        self.nome = '/'
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.tabela = {}

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
        return self.tabela[nome]

    def is_full(self):
        return len(self.tabela) >= 392

    def tem(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        return nome in self.tabela.keys()

    def load(self, file):
        file.seek(58000)
        dado = file.read(4000)
        self.nome = dado[0:8].replace(b'\x00', b'').decode()
        self.access = dado[8:32].decode()
        self.modify = dado[32:56].decode()
        self.create = dado[56:80].decode()
        self.tabela = dict()
        for start in range(80, 4000, 10):
            nome = dado[start:start+8].replace(b'\x00', b'').decode()
            index = int.from_bytes(dado[start+8:start+10], sys.byteorder)
            if nome is not '':
                self.tabela[nome] = index

    def save(self, file):
        file.seek(58000)
        dado = self.nome.encode('ascii', 'replace').rjust(8, b'\x00')
        dado += self.access.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.create.encode('ascii', 'replace')
        for nome, index in self.tabela.items():
            dado += nome.encode('ascii', 'replace').rjust(8, b'\x00')
            dado += index.to_bytes(2, sys.byteorder)
        dado += b'\x00' * (len(dado) % 4000)
        file.write(dado)
