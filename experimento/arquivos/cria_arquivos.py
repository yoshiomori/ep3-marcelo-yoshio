import ep3


def insere_arquivos():
    # Criando o diretório pai com 30 níveis
    for i in range(30):
        ep3.mkdir('/pai_sem/' + 'subdir/' * i)

    # Criando o diretório pai com 30 níveis de hierarquia com centenas de arquivos regulares em todos os
    # subdiretórios
    for i in range(30):
        caminho = '/pai_com/' + 'subdir/' * i
        ep3.mkdir(caminho)
        for j in range(100):
            ep3.touch(caminho + 'arquivo%d' % j)


def cria_arquivos():
    nome_arquivos = ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']
    # Criando um arquivo de 1MB, 10MB e 30MB
    for nome_arquivo, tamanho in zip(nome_arquivos, [10**6, 10*10**6, 30*10**6]):
        arquivo = open(nome_arquivo, 'wb')
        arquivo.write(b'\x00' * tamanho)  # Criando um arquivo com tamanho bytes
        arquivo.close()

    ep3.mount('sistema_vazio')
    insere_arquivos()
    ep3.umount()

    ep3.mount('sistema_10MB')
    ep3.cp('arquivo10MB', '/carga10MB')
    insere_arquivos()
    ep3.umount()

    ep3.mount('sistema_50MB')
    ep3.cp('arquivo10MB', 'carga1')
    ep3.cp('arquivo10MB', 'carga2')
    ep3.cp('arquivo30MB', 'carga3')
    insere_arquivos()
    ep3.umount()

if __name__ == '__main__':
    cria_arquivos()
