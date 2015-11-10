from time import asctime

from fat import Fat
from mapa_bits import BitMap


class Root(object):
    def __init__(self, bitmap, fat):
        self.nome = '/'
        self.access = asctime()
        self.modify = asctime()
        self.create = asctime()
        self.tabela = {}
        if type(bitmap) is not BitMap:
            raise TypeError('type bitmap is not BitMap')
        self.mapa_bits = bitmap
        if type(fat) is not Fat:
            raise TypeError('type fat is not Fat')
        self.fat = fat

    def set_name(self, nome):
        if type(nome) is not str:
            raise TypeError('type nome is not str')
        self.modify = asctime()
        self.access = asctime()
        self.nome = nome
