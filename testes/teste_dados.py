from arquivo import ArquivosRegulares

arquivo = ArquivosRegulares()
arquivo.set('teste', 'olá', [0])
file = open('dados_test', 'wb')
arquivo.save(file)
file.close()
arquivo = ArquivosRegulares()
file = open('dados_test', 'rb')
arquivo.load(file, [0])
file.close()
print('arquivo.load(file, [0])->arquivo.get_nome() =', arquivo.get_nome(), 'Espero teste')
print('arquivo.get_dado() =', arquivo.get_dado(), 'Espero ol?')
