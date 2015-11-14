from time import asctime
import sys


class Root(object):
    def __init__(self):
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
        if len(self.tabela) > 15:
            raise RuntimeError('Tabela excedeu tamanho máximo 15')
        self.access = asctime()
        self.tabela[nome] = index

    def del_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        if len(self.tabela) > 15:
            raise RuntimeError('Tabela excedeu tamanho máximo 15')
        self.access = asctime()
        try:
            return self.tabela.pop(nome)
        except KeyError:
            raise FileNotFoundError()

    def get_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        try:
            return self.tabela[nome]
        except KeyError:
            print(nome, 'arquivo ou diretório não existe')
            raise FileNotFoundError()

    def is_full(self):
        return len(self.tabela) >= 392

    def tem(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        return nome in self.tabela.keys()

    def load(self, file):
        file.seek(56000)
        dado = file.read(4000)
        if self.tipo != dado[0:1]:
            raise RuntimeError('Dado não compatível')
        self.nome = dado[1:256].replace(b'\x00', b'').decode()
        self.access = dado[256:280].decode()
        self.modify = dado[280:304].decode()
        self.create = dado[304:328].decode()
        self.tabela = dict()
        for start in range(328, 4000, 257):
            nome = dado[start:start+255].replace(b'\x00', b'').decode()
            index = int.from_bytes(dado[start+255:start+257], sys.byteorder)
            if nome is not '':
                self.tabela[nome] = index

    def save(self, file):
        file.seek(56000)
        dado = self.tipo
        dado += self.nome.encode('ascii', 'replace').rjust(255, b'\x00')
        dado += self.access.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.create.encode('ascii', 'replace')
        for nome, index in self.tabela.items():
            dado += nome.encode('ascii', 'replace').rjust(255, b'\x00')
            dado += index.to_bytes(2, sys.byteorder)
        dado += b'\x00' * (len(dado) % 4000)
        file.write(dado)

    def keys(self):
        return self.tabela.keys()
