from fat import Fat
f1 = Fat()
print('f1.get(4242) =', f1.get(4242), 'Espero -1')
f1.set(4242, 4242)
print('f1.set(4242, 4242) -> f1.get(4242) =', f1.get(4242), 'Espero 4242')

f2 = Fat()
f2.parse_load(f1.save_format())
print('f2.load() -> f2.get(4242) =', f2.get(4242), 'Espero 4242')
