from time import asctime
import sys


class ArquivosRegulares(object):
    def __init__(self):
        self.tipo = b'\x00'
        self.nome = ''
        self.tamanho = 0
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.dado = ''

    def novo(self, nome, dado):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        if type(dado) is not str:
            raise TypeError('type dado is not str')
        self.nome = nome
        self.tamanho = len(dado)
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.dado = dado

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        self.access = asctime()
        self.modify = asctime()
        self.nome = nome

    def get_nome(self):
        return self.nome

    def set(self, nome, dado):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        if type(dado) is not str:
            raise TypeError('type dado is not str')
        if nome is '':
            raise TypeError("nome não pode ser ''")
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

    def parse_load(self, dado):
        if type(dado) is not bytes:
            raise TypeError('dado is not bytes')
        self.nome = dado[1:256].replace(b'\x00', b'').decode()
        self.tamanho = int.from_bytes(dado[256:260], sys.byteorder)
        self.create = dado[260:284].decode()
        self.modify = dado[284:308].decode()
        self.access = dado[308:332].decode()
        self.dado = dado[332:332 + self.tamanho].decode()

    def save_format(self):
        dado = self.tipo
        dado += self.nome.encode('ascii', 'replace').rjust(255, b'\x00')
        dado += self.tamanho.to_bytes(4, sys.byteorder)
        dado += self.create.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.access.encode('ascii', 'replace')
        dado += self.dado.encode('ascii', 'replace')
        return dado


class Directory(object):
    def __init__(self):
        self.tipo = b'\xff'
        self.nome = ''
        self.access = ''
        self.modify = ''
        self.create = ''
        self.tabela = {}

    def mkdir(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        self.nome = nome
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.tabela = {}

    def get_nome(self):
        return self.nome

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        self.modify = asctime()
        self.access = asctime()
        self.nome = nome

    def add_entry(self, nome, index):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        if type(index) is not int:
            raise TypeError('type index is not int')
        if index < 0 or 24984 < index:
            raise RuntimeError('index deve estar entre 0 e 24984')
        self.access = asctime()
        self.tabela[nome] = index

    def del_entry(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
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
            print('Arquivo ou diretório não encontrado')
            raise FileNotFoundError()

    def tem(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            print('nome excedeu tamanho máximo(255 Bytes)')
            raise RuntimeWarning('nome excedeu tamanho máximo(255)')
        return nome in self.tabela.keys()

    def keys(self):
        return self.tabela.keys()

    def parse_load(self, dado):
        self.nome = dado[1:256].replace(b'\x00', b'').decode()
        self.access = dado[256:280].decode()
        self.modify = dado[280:304].decode()
        self.create = dado[304:328].decode()
        self.tabela = dict()
        for start in range(328, 4000, 257):
            nome = dado[start:start+255].replace(b'\x00', b'').decode()
            index = int.from_bytes(dado[start+255:start+257], sys.byteorder)
            if nome is not '':
                if index >= 24985:
                    raise NotADirectoryError()  # É usado para identificar um arquivo
                self.tabela[nome] = index

    def save_format(self):
        dado = self.tipo
        dado += self.nome.encode('ascii', 'replace').rjust(255, b'\x00')
        dado += self.access.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.create.encode('ascii', 'replace')
        for nome, index in self.tabela.items():
            dado += nome.encode('ascii', 'replace').rjust(255, b'\x00')
            dado += index.to_bytes(2, sys.byteorder)
        dado += b'\x00' * (len(dado) % 4000)  # Na hora de salvar é importante zerar o resto para mostra que é diretório
        return dado
