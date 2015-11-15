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
    if arquivo is None:
        print('mount precisa de argumento')
        return
    if arquivo is None:
        print('O comando mount precisa de nome de arquivo como argumento')
        return
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
    if origem is None:
        print('origem faltando')
        return
    if destino is None:
        print('destino faltando')
        return
    if origem is None or destino is None:
        print('O comando precisa de 2 argumentos')
        return
    try:
        dados, caminho_destino, nome_destino = pega_dados(destino)
    except FileNotFoundError:
        return

    if nome_destino is None:
        _, nome_destino = parse_path(origem)

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
    if diretorio is None:
        print('mkdir precisa de um argumento')
        return
    try:
        dados, caminho_destino, nome_diretorio = pega_dados(diretorio)
    except FileNotFoundError:
        return

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
    while index != -1:
        bitmap.set_1(index)
        index = fat.get(index)


def rmdir(diretorio):
    if diretorio is None:
        print('rmdir precisa de um argumento')
        return
    try:
        dados, caminho_destino, nome_diretorio = pega_dados(diretorio)
    except FileNotFoundError:
        return
    if dados.tem(nome_diretorio):
        index = dados.get_entry(nome_diretorio)
        arquivo = Dados(bitmap, fat, index)
        arquivo.load(unidade)
        if not arquivo.is_dir():
            print('Não é diretório')
            return
        dados.del_entry(nome_diretorio)
        dados.save(unidade)
        for arquivos in arquivo.keys():
            index = arquivo.get_entry(arquivos)
            dado = Dados(bitmap, fat, index)
            dado.load(unidade)
            if dado.is_dir():
                rmdir_recursivo(index)
            else:
                while index != -1:
                    bitmap.set_1(index)
                    index = fat.get(index)
        print(nome_diretorio,
              '%s removido%s com sucesso' % ('foram', 's') if len(dados.keys())
              else '%s removido%s com sucesso' % ('foi', ''))
    else:
        print('Diretório %s não existe' % nome_diretorio)

    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def pega_dados(nome_arquivo):
    caminho = nome_arquivo.split('/')
    while '' in caminho:
        caminho.remove('')
    if len(caminho) == 0:
        return root, caminho, None
    nome_arquivo = caminho.pop()
    diretório = root
    for nome_diretório in caminho:
        if not diretório.tem(nome_diretório):
            print('Diretório não foi encontrado')
            raise FileNotFoundError
        diretório = Dados(bitmap, fat, diretório.get_entry(nome_diretório))
        diretório.load(unidade)
        if not diretório.is_dir():
            print(diretório.get_nome(), 'é um arquivo')
            raise NotADirectoryError
    return diretório, caminho, nome_arquivo


def cat(arquivo):
    if arquivo is None:
        print('cat precisa de um argumento')
        return
    try:
        dados, caminho_destino, nome_arquivo = pega_dados(arquivo)
    except FileNotFoundError:
        return
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
    if arquivo is None:
        print('touch precisa de um argumento')
        return
    try:
        dados, caminho_destino, nome_arquivo = pega_dados(arquivo)
    except FileNotFoundError:
        return
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
    if arquivo is None:
        print('rm precisa de um argumento')
        return
    dados, caminho_destino, nome_arquivo = pega_dados(arquivo)
    if nome_arquivo in dados.keys():
        index = dados.get_entry(nome_arquivo)
        arquivo = Dados(bitmap, fat, index)
        arquivo.load(unidade)
        if arquivo.is_dir():
            print('É um diretório')
            return
        while index != -1:
            bitmap.set_1(index)
            index = fat.get(index)
        dados.del_entry(nome_arquivo)
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
    if diretorio is None:
        print('ls precisa de um argumento')
        return
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
            print('É um arquivo.')
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def find_recursive(dados, caminho_destino, arquivo_procurado):
    for nome_arquivo in dados.keys():
        index = dados.get_entry(nome_arquivo)
        arquivo = Dados(bitmap, fat, index)
        arquivo.load(unidade)
        if arquivo.is_dir():
            find_recursive(arquivo, caminho_destino + [nome_arquivo], arquivo_procurado)
        else:
            if arquivo.get_nome() == arquivo_procurado:
                print('/' + '/'.join(caminho_destino) + '/' + arquivo_procurado)
                return


def find(diretorio, arquivo):
    if diretorio is None or arquivo is None:
        print('find precisa de dois argumentos')
        return
    dados, caminho_destino, diretorio = pega_dados(diretorio)
    if diretorio is not None:
        if not dados.tem(diretorio):
            print('Diretório não encontrado')
            return
        index = dados.get_entry(diretorio)
        dados = Dados(bitmap, fat, index)
        dados.load(unidade)
        if not dados.is_dir():
            print('Não é um diretório')
            return
        find_recursive(dados, caminho_destino + [diretorio], arquivo)
    else:
        find_recursive(dados, caminho_destino, arquivo)
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def df():
    quantidade_diretórios = 1
    quantidade_arquivos = 0
    espaço_livre = 99940000
    espaço_desperdiçado = 224  # 224 B desperdiçado nos metadados
    pilha = []

    # Tratamento especial para o root
    for nome_arquivo in root.keys():
        index = root.get_entry(nome_arquivo)
        arquivo = Dados(bitmap, fat, index)
        arquivo.load(unidade)
        if arquivo.is_dir():
            quantidade_diretórios += 1
            # 328 bytes para o cabeçalho do diretório e cada linha ocupa 257 bytes
            espaço_desperdiçado += 4000 - arquivo.get_len_tabela() * 257 - 328
            pilha.append(arquivo)
        else:
            quantidade_arquivos += 1
            espaço_desperdiçado += 4000 - arquivo.get_tamanho() - 332  # 332 bytes para o cabeçalho do diretório
        espaço_livre -= 4000

    while len(pilha):
        dado = pilha.pop()
        for nome_arquivo in dado.keys():
            index = dado.get_entry(nome_arquivo)
            arquivo = Dados(bitmap, fat, index)
            arquivo.load(unidade)
            if arquivo.is_dir():
                quantidade_diretórios += 1
                # 328 bytes para o cabeçalho do diretório e cada linha ocupa 257 bytes
                espaço_desperdiçado += 4000 - dado.get_len_tabela() * 257 - 328
                pilha.append(arquivo)
            else:
                quantidade_arquivos += 1
                espaço_desperdiçado += 4000 - dado.get_tamanho() - 332  # 332 bytes para o cabeçalho do diretório
            espaço_livre -= 4000
    print('quantidade diretórios:', quantidade_diretórios)
    print('quantidade arquivos:', quantidade_arquivos)
    print('espaço livre:', espaço_livre)
    print('espaço desperdiçado:', espaço_desperdiçado)  # 224 B desperdiçado nos metadados)


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
