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
    caminho = caminho_destino.split('/')
    nome_diretorio = caminho.pop(0)
    index = fat[root.get_entry(nome_diretorio)]
    while len(caminho):
        dados = Dados(bitmap, fat, 'diretorio', index)
        try:
            dados.load(unidade)
        except NotADirectoryError:
            print(nome_diretorio, 'não é diretório')
            raise RuntimeWarning()
        index = dados.arquivo.get_entry(caminho.pop(0))
    dados = Dados(bitmap, fat, 'diretorio', index)
    dados.load(unidade)
    return dados


def cp(origem, destino):
    caminho_destino, sep, nome_destino = destino.rpartition('/')
    
    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_destino)
    
    # É necessário o índice inicial ser alocado aqui, porque esse indice vai ser usado tanto como entrada no diretório
    # correspondente quanto como primeiro índice do bloco do arquivo copiado.
    index = aloca()
    
    # Adicionando o novo arquivo como entrada do diretório destino
    dados.arquivo.set_entry(nome_destino, index)
    dados.save(unidade)
    
    # Criando um novo arquivo com o mesmo indice da entrada adicionado do diretório com os dados copiados do arquivo
    dados = Dados(bitmap, fat, 'arquivo', index)
    file = open(origem)
    dados.arquivo.set(nome_destino, file.read())
    file.close()
    dados.save(unidade)
    
    # Em cada operação devemos salvar o estado dos metadados
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def mkdir(diretorio):
    caminho_diretorio, sep, nome_diretorio = diretorio.rpartition('/')
    
    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_diretorio)
    
    # É necessário o índice inicial ser alocado aqui, porque esse indice vai ser usado tanto como entrada no diretório
    # correspondente quanto como primeiro índice do bloco do arquivo copiado.
    index = aloca()
    
    # Adicionando o índice do primeiro bloco da sequencia do novo arquivo como entrada do diretório destino
    dados.arquivo.set_entry(nome_diretorio, index)
    dados.save(unidade)
    
    # Criando um diretorio vazio com o indice adicionado na entrada do outro diretório
    dados = Dados(bitmap, fat, 'diretorio', index)
    dados.save(unidade)
    
    # Em cada operação devemos salvar o estado dos metadados
    bitmap.save(unidade)
    fat.save(unidade)
    root.save(unidade)


def rmdir(diretorio):
    caminho_diretorio, sep, nome_diretorio = diretorio.rpartition('/')

    # Retorna um objeto do tipo Dados para diretório
    dados = percorre_caminho(caminho_diretorio)

    if dados.arquivo.tem(nome_diretorio):
        index = dados.arquivo.del_entry(nome_diretorio)
        dados.save(unidade)

        dados = Dados(bitmap, fat, 'diretorio', index)
        for arquivos in dados.arquivo.keys():
            rmdir_recursivo(dados, )



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
