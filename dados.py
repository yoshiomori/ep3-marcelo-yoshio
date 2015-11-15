from math import ceil
from time import asctime
import sys


class Dados(object):
    def __init__(self, bitmap=None, fat=None, index=-1):
        self.tipo = None
        self.nome = ''
        self.tamanho = 0
        self.access = ''
        self.modify = ''
        self.create = ''
        self.dado = ''
        self.tabela = {}
        self.indexes = []
        self.last_index = index
        self.bitmap = bitmap
        self.fat = fat

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
        self.tipo = b'\x00'
        self.nome = nome
        self.create = asctime()
        self.modify = asctime()
        self.access = asctime()
        self.dado = dado
        self.tamanho = len(dado)

    def get_dado(self):
        self.access = asctime()
        return self.dado

    def parse_load_arq(self, dado):
        self.tipo = dado[0:1]
        self.nome = dado[1:256].replace(b'\x00', b'').decode()
        self.tamanho = int.from_bytes(dado[256:260], sys.byteorder)
        self.create = dado[260:284].decode()
        self.modify = dado[284:308].decode()
        self.access = dado[308:332].decode()
        self.dado = dado[332:332 + self.tamanho].decode()

    def parse_load_dir(self, dado):
        self.tipo = dado[0:1]
        self.nome = dado[1:256].replace(b'\x00', b'').decode()
        self.create = dado[256:280].decode()
        self.modify = dado[280:304].decode()
        self.access = dado[304:328].decode()
        self.tabela = dict()
        for start in range(328, 4000 * len(self.indexes + [self.last_index]), 257):
            nome = dado[start:start+255].replace(b'\x00', b'').decode()
            index = int.from_bytes(dado[start+255:start+257], sys.byteorder)
            if nome is not '':
                if index >= 24985:
                    raise NotADirectoryError()  # É usado para identificar um arquivo
                self.tabela[nome] = index

    def save_format_arq(self):
        dado = self.tipo
        dado += self.nome.encode('ascii', 'replace').rjust(255, b'\x00')
        dado += self.tamanho.to_bytes(4, sys.byteorder)
        dado += self.create.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.access.encode('ascii', 'replace')
        dado += self.dado.encode('ascii', 'replace')
        return dado

    def save_format_dir(self):
        dado = self.tipo
        dado += self.nome.encode('ascii', 'replace').rjust(255, b'\x00')
        dado += self.access.encode('ascii', 'replace')
        dado += self.modify.encode('ascii', 'replace')
        dado += self.create.encode('ascii', 'replace')
        for nome, index in self.tabela.items():
            dado += nome.encode('ascii', 'replace').rjust(255, b'\x00')
            dado += index.to_bytes(2, sys.byteorder)
        # Na hora de salvar é importante zerar o resto para mostra que é diretório
        dado += b'\x00' * (4000 - len(dado) % 4000)
        return dado

    def mkdir(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        if len(nome) > 255:
            raise RuntimeError('nome excedeu tamanho máximo(255)')
        self.tipo = b'\xff'
        self.nome = nome
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

    def load(self, file):
        while self.fat.get(self.last_index) != -1:
            self.indexes.append(self.last_index)
            self.last_index = self.fat.get(self.last_index)
        data = b''
        for index in self.indexes + [self.last_index]:
            file.seek(60000 + index * 4000)
            data += file.read(4000)
        if data[0:1] == b'\xff':
            self.parse_load_dir(data)
        elif data[0:1] == b'\x00':
            self.parse_load_arq(data)
        else:
            raise RuntimeError('Arquivo Corrompido')

    def save(self, file):
        if self.last_index is not -1:
            if self.tipo == b'\xff':
                dado = self.save_format_dir()
            elif self.tipo == b'\x00':
                dado = self.save_format_arq()
            else:
                raise RuntimeError('Arquivo Corrompido')
            if len(self.indexes) + 1 < ceil(len(dado) / 4000):
                for index in range(24985):
                    if self.bitmap.get(index):
                        self.bitmap.set_0(index)
                        self.fat.set(self.last_index, index)
                        self.indexes.append(self.last_index)
                        self.last_index = index
                        if len(self.indexes) + 1 == ceil(len(dado) / 4000):
                            self.fat.set(self.last_index, -1)
                            break
                    if index == 24984:
                        raise MemoryError('Sem espaço')
            while len(self.indexes) + 1 > ceil(len(dado) / 4000):
                self.bitmap.set_1(self.last_index)
                self.last_index = self.indexes.pop()
                self.fat[self.last_index] = -1
            start = 0
            for index in self.indexes:
                file.seek(60000 + index * 4000)
                file.write(dado[start:start+4000])
                start += 4000
            file.seek(60000 + self.last_index * 4000)
            file.write(dado[start:])
        else:
            file.seek(60000)
            file.write(b'\x00' * 99940000)

    def is_dir(self):
        return self.tipo == b'\xff'

    def get_len_tabela(self):
        return len(self.tabela)

    def get_tamanho(self):
        return self.tamanho

    def carrega_cabeçalho(self, file):
        file.seek(60000 + (self.indexes + [self.last_index])[0] * 4000)
        data = file.read(256)
        self.parse_load_cabeçalho(data)

    def parse_load_cabeçalho(self, dado):
        self.tipo = dado[0:1]
        self.nome = dado[1:256].replace(b'\x00', b'').decode()
