from arquivo import ArquivosRegulares, Directory
from root import Root
from mapa_bits import BitMap
from fat import Fat
from dados import Dados
unidade = None
bitmap = BitMap()
fat = Fat()
root = Root()


def mount(arquivo):
    global unidade
    try:
        unidade = open(arquivo, 'r+b')
        bitmap.load(unidade)
        fat.load(unidade)
        root.load(unidade)
    except FileNotFoundError:
        unidade = open(arquivo, 'w+b')
        bitmap.save(unidade)
        fat.save(unidade)
        root.save(unidade)
        Dados().save(unidade)


def percorre_caminho(caminho_destino):
    if len(caminho_destino) == 0:
        return root
    nome_diretorio = caminho_destino.pop(0)
    index = fat.get(root.get_entry(nome_diretorio))
    while len(caminho_destino):
        dados = Dados(bitmap, fat, 'diretorio', index)
        try:
            dados.load(unidade)
        except NotADirectoryError:
            print(nome_diretorio, 'não é diretório')
            raise RuntimeWarning()
        index = dados.arquivo.get_entry(caminho_destino.pop(0))
    dados = Dados(bitmap, fat, 'diretorio', index)
    dados.load(unidade)
    return dados


def aloca():
    for index in range(24985):
        if bitmap.get(index):
            bitmap.set_0(index)
            fat.set(index, -1)
            return index
    raise MemoryError('Sem espaço')


def cp(origem, destino):
    caminho_destino, nome_destino = parse_path(destino)

    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_destino)

    if dados.tem(nome_destino):
        print('Este Arquivo já existe')
        return

    # É necessário o índice inicial ser alocado aqui, porque esse indice vai ser usado tanto como entrada no diretório
    # correspondente quanto como primeiro índice do bloco do arquivo copiado.
    index = aloca()

    # Adicionando o novo arquivo como entrada do diretório destino
    dados.add_entry(nome_destino, index)
    dados.save(unidade)
    
    # Criando um novo arquivo com o mesmo indice da entrada adicionado do diretório com os dados copiados do arquivo
    dados = Dados(bitmap, fat, 'arquivo', index)
    file = open(origem)
    dados.set(nome_destino, file.read())
    file.close()
    dados.save(unidade)
    
    # Em cada operação devemos salvar o estado dos metadados
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def parse_path(destino):
    caminho_destino = []
    for s in destino.split('/'):
        if s is not '':
            caminho_destino.append(s)
    nome_destino = caminho_destino.pop()
    return caminho_destino, nome_destino


def mkdir(diretorio):
    caminho_destino, nome_diretorio = parse_path(diretorio)

    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_destino)

    if dados.tem(nome_diretorio):
        print('Já existe este diretório')
        return
    
    # É necessário o índice inicial ser alocado aqui, porque esse indice vai ser usado tanto como entrada no diretório
    # correspondente quanto como primeiro índice do bloco do arquivo copiado.
    index = aloca()
    
    # Adicionando o índice do primeiro bloco da sequencia do novo arquivo como entrada do diretório destino
    dados.add_entry(nome_diretorio, index)
    dados.save(unidade)
    
    # Criando um diretorio vazio com o indice adicionado na entrada do outro diretório
    dados = Dados(bitmap, fat, 'diretorio', index)
    dados.mkdir(nome_diretorio)
    dados.save(unidade)
    
    # Em cada operação devemos salvar o estado dos metadados
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def rmdir_recursivo(index):
    dados = Dados(bitmap, fat, 'diretorio', index)
    dados.load(unidade)
    for arquivos in dados.arquivo.keys():
        index = dados.get_entry(arquivos)
        rmdir_recursivo(index)
    while index is not -1:
        bitmap.set_1(index)
        index = fat.get(index)


def rmdir(diretorio):
    caminho_destino, nome_diretorio = parse_path(diretorio)

    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_destino)

    if dados.tem(nome_diretorio):
        index = dados.del_entry(nome_diretorio)
        dados.save(unidade)

        dados = Dados(bitmap, fat, 'diretorio', index)
        dados.load(unidade)
        for arquivos in dados.arquivo.keys():
            index = dados.get_entry(arquivos)
            rmdir_recursivo(index)
        bitmap.set_1(index)

    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def cat(arquivo):
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def touch(arquivo):
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def rm(arquivo):
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def ls(diretorio):
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def find(diretorio, arquivo):
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def df():
    pass


def umount():
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    unidade.close()


def main():
    while True:
        comando, sep, argumentos = input('[ep3] ').partition(' ')
        try:
            if comando == 'mount':
                mount(argumentos)
            elif comando == 'cp':
                origem, sep, destino = argumentos.partition(' ')
                cp(origem, destino)
            elif comando == 'mkdir':
                mkdir(argumentos)
            elif comando == 'rmdir':
                rmdir(argumentos)
            elif comando == 'cat':
                cat(argumentos)
            elif comando == 'touch':
                touch(argumentos)
            elif comando == 'rm':
                rm(argumentos)
            elif comando == 'ls':
                ls(argumentos)
            elif comando == 'find':
                diretorio, sep, arquivo = argumentos.partition(' ')
                find(diretorio, arquivo)
            elif comando == 'df':
                df()
            elif comando == 'umount':
                umount()
            elif comando == 'sai':
                break
            else:
                print('Comando possíveis:')
                print('mount, cp, mkdir, cat, touch, rm, ls, find, df, umount, sai')
        except RuntimeWarning():
            print('Comando inválido')
if __name__ == '__main__':
    main()
