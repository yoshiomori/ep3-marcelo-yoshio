from mapa_bits import BitMap
bm = BitMap()
print('bit 4242 =', bm.get(4242), 'Tinha que ser 1')
bm.set_0(4242)
print('bm.set_0(bm.set_0(42)) -> bit 4242 =', bm.get(4242), 'Tinha que ser 0')
file = open('bit_map_test', 'wb')
bm.set_file(file)
bm.save()
file.close()


bm = BitMap()
print('bit 4242 =', bm.get(4242), 'Tinha que ser 1')
file = open('bit_map_test', 'rb')
bm.set_file(file)
bm.load()
file.close()
print('bm.load() -> bit 4242 =', bm.get(4242), 'Tinha que ser 0')
