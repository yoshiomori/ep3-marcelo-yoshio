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
    index = root.get_entry(nome_diretorio)
    while len(caminho_destino):
        dados = Dados(bitmap, fat, index)
        dados.load(unidade)
        if not dados.is_dir():
            print('Não é um diretório')
            raise NotADirectoryError
        index = dados.get_entry(caminho_destino.pop(0))
    dados = Dados(bitmap, fat, index)
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
    dados, caminho_destino, nome_destino = pega_dados(destino)

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
    dados = Dados(bitmap, fat, index)
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
    nome_destino = None
    for s in destino.split('/'):
        if s is not '':
            caminho_destino.append(s)
    if len(caminho_destino):
        nome_destino = caminho_destino.pop()
    return caminho_destino, nome_destino


def mkdir(diretorio):
    dados, caminho_destino, nome_diretorio = pega_dados(diretorio)

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
    dados = Dados(bitmap, fat, index)
    dados.mkdir(nome_diretorio)
    dados.save(unidade)
    
    # Em cada operação devemos salvar o estado dos metadados
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def rmdir_recursivo(index):
    dados = Dados(bitmap, fat, index)
    dados.load(unidade)
    nome = dados.get_nome()
    for arquivos in dados.keys():
        index = dados.get_entry(arquivos)
        rmdir_recursivo(index)
    print(nome)
    while index is not -1:
        bitmap.set_1(index)
        index = fat.get(index)


def rmdir(diretorio):
    dados, caminho_destino, nome_diretorio = pega_dados(diretorio)

    if dados.tem(nome_diretorio):
        index = dados.del_entry(nome_diretorio)
        dados.save(unidade)

        dados = Dados(bitmap, fat, index)
        dados.load(unidade)
        for arquivos in dados.keys():
            index = dados.get_entry(arquivos)
            rmdir_recursivo(index)
        bitmap.set_1(index)
        print(nome_diretorio,
              '%s removido%s com sucesso' % ('foram', 's') if len(dados.keys()) else ('foi', ''))
    else:
        print('Diretório %s não existe' % nome_diretorio)

    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def pega_dados(diretorio):
    caminho_destino, nome_diretorio = parse_path(diretorio)
    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_destino)
    return dados, caminho_destino, nome_diretorio


def cat(arquivo):
    dados, caminho_destino, nome_arquivo = pega_dados(arquivo)
    if dados.tem(nome_arquivo):
        index = dados.get_entry(nome_arquivo)
        dados = Dados(bitmap, fat, index)
        dados.load(unidade)
        print(dados.get_dado())
        dados.save(unidade)
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def touch(arquivo):
    dados, caminho_destino, nome_arquivo = pega_dados(arquivo)
    if dados.tem(nome_arquivo):
        index = dados.get_entry(nome_arquivo)
        dados = Dados(bitmap, fat, index)
        dados.load(unidade)
        if dados.is_dir():
            print('É um diretório!')
            return
        dados.get_dado()  # com o get_dado eu estou atualizando o instante de acesso
        dados.save(unidade)
    else:
        index = aloca()
        dados.add_entry(nome_arquivo, index)
        dados.save(unidade)
        dados = Dados(bitmap, fat, index)
        dados.set(nome_arquivo, '')
        dados.save(unidade)
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def rm(arquivo):
    dados, caminho_destino, nome_arquivo = pega_dados(arquivo)
    if nome_arquivo in dados.keys():
        index = dados.get_entry(nome_arquivo)
        while index != -1:
            bitmap.set_1(index)
            index = fat.get(index)
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)
    pass


def faça_ls(dados):
    for nome in dados.keys():
        index = dados.get_entry(nome)
        arquivo = Dados(bitmap, fat, index)
        arquivo.load(unidade)
        if arquivo.is_dir():
            print(arquivo.get_nome(), '/', sep='')
        else:
            print(arquivo.get_nome())


def ls(diretorio):
    dados, caminho_destino, nome_arquivo = pega_dados(diretorio)
    if nome_arquivo is None:
        faça_ls(dados)
    else:
        index = dados.get_entry(nome_arquivo)
        dados = Dados(bitmap, fat, index)
        dados.load(unidade)
        if dados.is_dir():
            faça_ls(dados)
        else:
            print('É um diretório.')
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
    estado = 'umount'
    while True:
        comando, sep, argumentos = input('[ep3] ').partition(' ')
        try:
            if comando == 'mount' and estado == 'umount':
                mount(argumentos)
                estado = 'mount'
            elif comando == 'cp' and estado == 'mount':
                origem, sep, destino = argumentos.partition(' ')
                cp(origem, destino)
            elif comando == 'mkdir' and estado == 'mount':
                mkdir(argumentos)
            elif comando == 'rmdir' and estado == 'mount':
                rmdir(argumentos)
            elif comando == 'cat' and estado == 'mount':
                cat(argumentos)
            elif comando == 'touch' and estado == 'mount':
                touch(argumentos)
            elif comando == 'rm' and estado == 'mount':
                rm(argumentos)
            elif comando == 'ls' and estado == 'mount':
                ls(argumentos)
            elif comando == 'find' and estado == 'mount':
                diretorio, sep, arquivo = argumentos.partition(' ')
                find(diretorio, arquivo)
            elif comando == 'df' and estado == 'mount':
                df()
            elif comando == 'umount' and estado == 'mount':
                umount()
                estado = 'umount'
            elif comando == 'sai':
                break
            elif estado == 'umount':
                print('Comando possíveis:')
                print('mount e sai')
            else:
                print('Comando possíveis:')
                print('mount, cp, mkdir, cat, touch, rm, ls, find, df, umount, sai')
        except RuntimeWarning:
            print('Comando inválido')
if __name__ == '__main__':
    main()
