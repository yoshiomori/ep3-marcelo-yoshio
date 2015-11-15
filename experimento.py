import os

import ep3
from time import time


# O sistemaVazio é o sistema de arquivos vazio
# O sistema10MB é o o sistema de arquivos com 10MB ocupados
# O sistema50MB é o sistema de arquivos com 50MB ocupados
# A execução dessa função requer que os sistemas de arquivos: sistemaVazio, sistema10MB e sistema50MB tenham sido
# devidamente inicializados

# calcula o tempo de execução para a operação com os argumentos
def tempo_op(op, args, r):
    instante_inicial = time()
    op(*args)
    file.write('%s %d' % (r, time() - instante_inicial))


def experimento():
    nome_arquivos = ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']
    # Criando um arquivo de 1MB, 10MB e 30MB
    for nome_arquivo, tamanho in zip(nome_arquivos, [10**6, 10*10**6, 30*10**6]):
        arquivo = open(nome_arquivo, 'wb')
        arquivo.write(b'\x00' * tamanho)  # Criando um arquivo com tamanho bytes
        arquivo.close()
    for k in range(30):
        estado = 'sistema vazio %d' % k
        ep3.mount(estado)
        for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
            tempo_op(ep3.cp, (nome_arquivo, '/'), estado + ' - ' + nome_arquivo + 'cp')
        for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
            tempo_op(ep3.rm, ('/' + nome_arquivo,), estado + ' - ' + nome_arquivo + 'rm')

        # Criando o diretório pai com 30 níveis
        for i in range(30):
            ep3.mkdir('/pai/' + 'subdir/' * i)

        tempo_op(ep3.rmdir, ('/pai',), estado + ' - rmdir sem arquivo')

        # Criando o diretório pai com 30 níveis de hierarquia com centenas de arquivos regulares em todos os
        # subdiretórios
        for i in range(30):
            caminho = '/pai/' + 'subdir/' * i
            ep3.mkdir(caminho)
            for j in range(100):
                ep3.touch(caminho + 'arquivo%d' % j)

        tempo_op(ep3.rmdir, ('/pai',), estado + ' - rmdir com arquivo')
        ep3.umount()
        os.remove(estado)

    for k in range(30):
        # Sistema de arquivos com 10MB ocupados
        estado = 'sistema 10MB ocupado %d' % k
        ep3.mount(estado)
        ep3.cp('arquivo10MB', '/ocupado10MB')
        for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
            tempo_op(ep3.cp, (nome_arquivo, '/'), estado + ' - ' + nome_arquivo + 'cp')
        for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
            tempo_op(ep3.rm, ('/' + nome_arquivo,), estado + ' - ' + nome_arquivo + 'rm')

        # Criando o diretório pai com 30 níveis
        for i in range(30):
            ep3.mkdir('/pai/' + 'subdir/' * i)

        tempo_op(ep3.rmdir, ('/pai',), estado + ' - rmdir sem arquivo')

        # Criando o diretório pai com 30 níveis de hierarquia com centenas de arquivos regulares em todos os
        # subdiretórios
        for i in range(30):
            caminho = '/pai/' + 'subdir/' * i
            ep3.mkdir(caminho)
            for j in range(100):
                ep3.touch(caminho + 'arquivo%d' % j)

        tempo_op(ep3.rmdir, ('/pai',), estado + ' - rmdir com arquivo')
        ep3.umount()
        os.remove(estado)

    for k in range(30):
        # Sistema de arquivos com 50MB ocupado
        estado = 'sistema 50MB ocupado %d' % k
        ep3.mount(estado)
        ep3.cp('arquivo10MB', '/ocupado1')
        ep3.cp('arquivo10MB', '/ocupado2')
        ep3.cp('arquivo30MB', '/ocupado3')
        for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
            tempo_op(ep3.cp, (nome_arquivo, '/'), estado + ' - ' + nome_arquivo + 'cp')
        for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
            tempo_op(ep3.rm, ('/' + nome_arquivo,), estado + ' - ' + nome_arquivo + 'rm')

        # Criando o diretório pai com 30 níveis
        for i in range(30):
            ep3.mkdir('/pai/' + 'subdir/' * i)

        tempo_op(ep3.rmdir, ('/pai',), estado + ' - rmdir sem arquivo')

        # Criando o diretório pai com 30 níveis de hierarquia com centenas de arquivos regulares em todos os
        #  subdiretórios
        for i in range(30):
            caminho = '/pai/' + 'subdir/' * i
            ep3.mkdir(caminho)
            for j in range(100):
                ep3.touch(caminho + 'arquivo%d' % j)

        tempo_op(ep3.rmdir, ('/pai',), estado + ' - rmdir com arquivo')
        ep3.umount()
        os.remove(estado)
    
if __name__ == '__main__':
    file = open('resultado', 'w')
    try:
        experimento()
    except MemoryError:
        pass
    file.close()
