from time import asctime
import sys

from dados import Dados


class Root(Dados):
    def __init__(self):
        super().__init__()
        self.tipo = b'\xff'
        self.nome = '/'
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.tabela = {}

    def add_entry(self, nome, index):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        if type(index) is not int:
            raise TypeError('type index is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        if len(self.tabela) > 26:
            raise RuntimeError('Tabela excedeu tamanho máximo 26')
        self.access = asctime()
        self.tabela[nome] = index

    def load(self, file):
        file.seek(53094)
        dado = file.read(6906)
        self.access = dado[:24].decode()
        self.modify = dado[24:48].decode()
        self.create = dado[48:72].decode()
        self.tabela = dict()
        for start in range(72, 6906, 257):
            nome = dado[start:start+255].replace(b'\x00', b'').decode()
            index = int.from_bytes(dado[start+255:start+257], sys.byteorder)
            if nome is not '':
                self.tabela[nome] = index

    def save(self, file):
        file.seek(53094)
        dado = self.access.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.create.encode('ascii', 'replace')
        for nome, index in self.tabela.items():
            dado += nome.encode('ascii', 'replace').rjust(255, b'\x00')
            dado += index.to_bytes(2, sys.byteorder)
        dado += b'\x00' * (6906 - len(dado) % 6906)
        file.write(dado)
