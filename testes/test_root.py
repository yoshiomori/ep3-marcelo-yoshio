from root import Root


root1 = Root()
root1.add_entry('var', 0)

root2 = Root()
root2.parse_load(root1.save_format())
print("root.load() -> root.tabela['var'] =", root2.tabela['var'], 'Espero 0')
print('root.is_full() =', root2.is_full(), 'Espero False')
if root2.tem('var'):
    root2.del_entry('var')
print("root.tem('var') =", root2.tem('var'), 'Espero False')
