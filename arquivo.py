from time import asctime
import sys


class ArquivosRegulares(object):
    def __init__(self, nome, dado):
        self.nome = nome
        self.tamanho = len(dado)
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.dado = dado

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        self.access = asctime()
        self.modify = asctime()
        self.nome = nome

    def get_nome(self):
        return self.nome

    def set(self, nome, dado):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if type(dado) is not str:
            raise TypeError('type dado is not str')
        self.nome = nome
        self.create = asctime()
        self.modify = asctime()
        self.access = asctime()
        self.dado = dado
        self.tamanho = len(dado)

    def set_dado(self, dado):
        if type(dado) is not str:
            raise TypeError('type dado is not str')
        self.modify = asctime()
        self.access = asctime()
        self.dado = dado
        self.tamanho = len(dado)

    def get_dado(self):
        self.access = asctime()
        return self.dado

    def load_parse(self, dado):
        if type(dado) is not bytes:
            raise TypeError('dado is not bytes')
        self.nome = dado[0:8].replace(b'\x00', b'').decode()
        self.tamanho = int.from_bytes(dado[8:12], sys.byteorder)
        self.create = dado[12:36].decode()
        self.modify = dado[36:60].decode()
        self.access = dado[60:84].decode()
        self.dado = dado[84:84 + self.tamanho].decode()

    def save_format(self):
        dado = self.nome.encode('ascii', 'replace').rjust(8, b'\x00')
        dado += self.tamanho.to_bytes(4, sys.byteorder)
        dado += self.create.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.access.encode('ascii', 'replace')
        dado += self.dado.encode('ascii', 'replace')
        return dado


class Directory(object):
    def __init__(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        self.nome = nome
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.tabela = {}

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        self.modify = asctime()
        self.access = asctime()
        self.nome = nome

    def add_entry(self, nome, index):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        if type(index) is not int:
            raise TypeError('type index is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        self.access = asctime()
        self.tabela[nome] = index

    def del_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        self.access = asctime()
        self.tabela.pop(nome)

    def get_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        return self.tabela[nome]

    def tem(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 8:
            raise RuntimeError('nome excedeu tamanho máximo(8)')
        return nome in self.tabela.keys()

    def parse_load(self, dado):
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

    def save_format(self):
        dado = self.nome.encode('ascii', 'replace').rjust(8, b'\x00')
        dado += self.access.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.create.encode('ascii', 'replace')
        for nome, index in self.tabela.items():
            dado += nome.encode('ascii', 'replace').rjust(8, b'\x00')
            dado += index.to_bytes(2, sys.byteorder)
        dado += b'\x00' * (len(dado) % 4000)
