from root import Root


root = Root()
root.set_table('var', 0)
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
