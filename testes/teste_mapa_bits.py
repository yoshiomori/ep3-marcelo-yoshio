from mapa_bits import BitMap
bm1 = BitMap()
print('bit 4242 =', bm1.get(4242), 'Tinha que ser 1')
bm1.set_0(4242)
print('bm.set_0(bm1.set_0(42)) -> bit 4242 =', bm1.get(4242), 'Tinha que ser 0')


bm2 = BitMap()
print('bit 4242 =', bm2.get(4242), 'Tinha que ser 1')
bm2.parse_load(bm1.save_format())
print('bm.load() -> bit 4242 =', bm2.get(4242), 'Tinha que ser 0')
