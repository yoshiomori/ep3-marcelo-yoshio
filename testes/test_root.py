from fat import Fat
from mapa_bits import BitMap
from root import Root

bitmap = BitMap()
fat = Fat()
root = Root(bitmap, fat)
bitmap.set_0(4242)
print('root.mapa_bits.get(4242) =', root.mapa_bits.get(4242), 'Espero 0')
