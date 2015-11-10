from root import Root


root = Root()
root.add_entry('var', 0)
file = open('root_test', 'wb')
root.set_file(file)
root.save()
file.close()

root = Root()
file = open('root_test', 'rb')
root.set_file(file)
root.load()
file.close()
print("root.load() -> root.tabela['var'] =", root.tabela['var'], 'Espero 0')
print('root.is_full() =', root.is_full(), 'Espero False')
if root.tem('var'):
    root.del_entry('var')
print("root.tem('var') =", root.tem('var'), 'Espero False')
