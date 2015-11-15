import ep3
from time import time


# O sistemaVazio é o sistema de arquivos vazio
# O sistema10MB é o o sistema de arquivos com 10MB ocupados
# O sistema50MB é o sistema de arquivos com 50MB ocupados
# A execução dessa função requer que os sistemas de arquivos: sistemaVazio, sistema10MB e sistema50MB tenham sido
# devidamente inicializados

# calcula o tempo de execução para a operação com os argumentos
def tempo_op(op, args):
    instante_inicial = time()
    op(*args)
    return time() - instante_inicial


def experimento():
    nome_arquivos = ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']
    # Criando um arquivo de 1MB, 10MB e 30MB
    for nome_arquivo, tamanho in zip(nome_arquivos, [10**6, 10*10**6, 30*10**6]):
        arquivo = open(nome_arquivo, 'wb')
        arquivo.write(b'\x00' * tamanho)  # Criando um arquivo com tamanho bytes
        arquivo.close()
    ep3.mount('sistemaVazio')
    intervalos = []
    for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
        intervalos.append(tempo_op(ep3.cp, (nome_arquivo, '/')))
    for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
        intervalos.append(tempo_op(ep3.rm, ('/' + nome_arquivo,)))

    # Criando o diretório pai com 30 níveis
    for i in range(30):
        ep3.mkdir('/pai/' + 'subdir/' * i)

    ep3.rmdir('/pai')

    # Criando o diretório pai com 30 níveis de hierarquia com centenas de arquivos regulares em todos os subdiretórios
    for i in range(30):
        caminho = '/pai/' + 'subdir/' * i
        ep3.mkdir(caminho)
        for j in range(100):
            ep3.touch(caminho + 'arquivo%d' % j)

    ep3.rmdir('/pai')
    ep3.umount()
