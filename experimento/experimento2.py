import math

import ep3
import sys
import os
from time import time


def cp(nome_origem, nome_destino):
    origem = open(nome_origem, 'rb')
    destino = open(nome_destino, 'wb')
    destino.write(origem.read())
    destino.close()
    origem.close()


# calcula o tempo de execução para a operação com os argumentos
def tempo_op(op, args):
    instante_inicial = time()
    op(*args)
    return time() - instante_inicial


def test_cp():
    for arquivo, nome_octave, titulo in zip(['arquivo1MB', 'arquivo10MB', 'arquivo30MB'], ['cp1MB', 'cp10MB', 'cp30MB'],
                                            ['Copia de 1MB', 'Copia de 10MB', 'Copia de 30MB']):
        médias = []
        menor = []
        maior = []
        mínimo = []
        máximo = []

        cp('arquivos/arquivo1MB', arquivo)
        for nome_sistema in ['sistema_vazio', 'sistema_10MB', 'sistema_50MB']:
            # Soma total
            valores = []
            mntcp = float('inf')
            mxtcp = float('-inf')

            for i in range(30):
                print('iteração %d' % i)
                cp('arquivos/' + nome_sistema, nome_sistema)
                ep3.mount(nome_sistema)
                t = tempo_op(ep3.cp, (arquivo, '/'))
                ep3.umount()
                valores.append(t)
                mntcp = min(mntcp, t)
                mxtcp = max(mxtcp, t)
                os.remove(nome_sistema)
            média = sum(valores) / 30
            médias.append(média)
            desvio = math.sqrt(sum([(x - média) ** 2 for x in valores]) / 30)
            menor.append(média - (-1.96) * desvio / math.sqrt(30))
            maior.append(média + (-1.96) * desvio / math.sqrt(30))
            mínimo.append(mntcp)
            máximo.append(mxtcp)
        os.remove(arquivo)
        f = open(nome_octave + '.m', 'w')
        f.write('x = [0, 10, 50];\n')
        f.write('media = %s;\n' % repr(médias))
        f.write('menor = %s;\n' % repr(menor))
        f.write('maior = %s;\n' % repr(maior))
        f.write('minimo = %s;\n' % repr(mínimo))
        f.write('maximo = %s;\n' % repr(máximo))
        f.write("plot(x,media,';media;', x, menor, 'g;menor;', x, maior, 'g;maior;', x, minimo, 'r;minimo;', x, maximo,"
                " 'r;maximo;')\n")
        f.write("title('%s')\n" % titulo)
        f.write("xlabel('Tamanho Ocupado do Sistema de Arquivo (MB)')\n")
        f.write("ylabel('Tempo Gasto (ms)')\n")
        f.close()


def test_rm():
    for arquivo, nome_octave, titulo in zip(['arquivo1MB', 'arquivo10MB', 'arquivo30MB'], ['rm1MB', 'rm10MB', 'rm30MB'],
                                            ['Remocao de 1MB', 'Remocao de 10MB', 'Remocao de 30MB']):
        médias = []
        menor = []
        maior = []
        mínimo = []
        máximo = []

        cp('arquivos/arquivo1MB', arquivo)
        for nome_sistema in ['sistema_vazio', 'sistema_10MB', 'sistema_50MB']:
            # Soma total
            valores = []
            mntcp = float('inf')
            mxtcp = float('-inf')

            for i in range(30):
                print('iteração %d' % i)
                cp('arquivos/' + nome_sistema, nome_sistema)
                ep3.mount(nome_sistema)
                ep3.cp(arquivo, '/')
                t = tempo_op(ep3.rm, (arquivo,))
                ep3.umount()
                valores.append(t)
                mntcp = min(mntcp, t)
                mxtcp = max(mxtcp, t)
                os.remove(nome_sistema)
            média = sum(valores) / 30
            médias.append(média)
            desvio = math.sqrt(sum([(x - média) ** 2 for x in valores]) / 30)
            menor.append(média - (-1.96) * desvio / math.sqrt(30))
            maior.append(média + (-1.96) * desvio / math.sqrt(30))
            mínimo.append(mntcp)
            máximo.append(mxtcp)
        os.remove(arquivo)
        f = open(nome_octave + '.m', 'w')
        f.write('x = [0, 10, 50];\n')
        f.write('media = %s;\n' % repr(médias))
        f.write('menor = %s;\n' % repr(menor))
        f.write('maior = %s;\n' % repr(maior))
        f.write('minimo = %s;\n' % repr(mínimo))
        f.write('maximo = %s;\n' % repr(máximo))
        f.write("plot(x,media,';media;', x, menor, 'g;menor;', x, maior, 'g;maior;', x, minimo, 'r;minimo;', x, maximo,"
                " 'r;maximo;')\n")
        f.write("title('%s')\n" % titulo)
        f.write("xlabel('Tamanho Ocupado do Sistema de Arquivo (MB)')\n")
        f.write("ylabel('Tempo Gasto (ms)')\n")
        f.close()


def test_rm_pai_sem():
    médias = []
    menor = []
    maior = []
    mínimo = []
    máximo = []
    for nome_sistema in ['sistema_vazio', 'sistema_10MB', 'sistema_50MB']:
        # Soma total
        valores = []
        mntcp = float('inf')
        mxtcp = float('-inf')

        for i in range(30):
            print('iteração %d' % i)
            cp('arquivos/' + nome_sistema, nome_sistema)
            ep3.mount(nome_sistema)
            # Criando o diretório pai com 30 níveis
            for i in range(30):
                ep3.mkdir('/pai/' + 'subdir/' * i)
            t = tempo_op(ep3.rmdir, ('/pai',))
            ep3.umount()
            valores.append(t)
            mntcp = min(mntcp, t)
            mxtcp = max(mxtcp, t)
            os.remove(nome_sistema)
        média = sum(valores) / 30
        médias.append(média)
        desvio = math.sqrt(sum([(x - média) ** 2 for x in valores]) / 30)
        menor.append(média - (-1.96) * desvio / math.sqrt(30))
        maior.append(média + (-1.96) * desvio / math.sqrt(30))
        mínimo.append(mntcp)
        máximo.append(mxtcp)
    f = open('rmpaisem.m', 'w')
    f.write('x = [0, 10, 50];\n')
    f.write('media = %s;\n' % repr(médias))
    f.write('menor = %s;\n' % repr(menor))
    f.write('maior = %s;\n' % repr(maior))
    f.write('minimo = %s;\n' % repr(mínimo))
    f.write('maximo = %s;\n' % repr(máximo))
    f.write("plot(x,media,';media;', x, menor, 'g;menor;', x, maior, 'g;maior;', x, minimo, 'r;minimo;', x, maximo,"
            " 'r;maximo;')\n")
    f.write("title('Remocao do diretorio pai com 30 subdiretorios')\n")
    f.write("xlabel('Tamanho Ocupado do Sistema de Arquivo (MB)')\n")
    f.write("ylabel('Tempo Gasto (ms)')\n")
    f.close()


def test_rm_pai_com():
    médias = []
    menor = []
    maior = []
    mínimo = []
    máximo = []
    for nome_sistema in ['sistema_vazio', 'sistema_10MB', 'sistema_50MB']:
        # Soma total
        valores = []
        mntcp = float('inf')
        mxtcp = float('-inf')

        for i in range(30):
            print('iteração %d' % i)
            cp('arquivos/' + nome_sistema, nome_sistema)
            ep3.mount(nome_sistema)
            # Criando o diretório pai com 30 níveis de hierarquia com centenas de arquivos regulares em todos os
            # subdiretórios
            for j in range(30):
                caminho = '/pai/' + 'subdir/' * j
                ep3.mkdir(caminho)
                for k in range(100):
                    ep3.touch(caminho + 'arquivo%d' % k)
            t = tempo_op(ep3.rmdir, ('/pai',))
            ep3.umount()
            valores.append(t)
            mntcp = min(mntcp, t)
            mxtcp = max(mxtcp, t)
            os.remove(nome_sistema)
        média = sum(valores) / 30
        médias.append(média)
        desvio = math.sqrt(sum([(x - média) ** 2 for x in valores]) / 30)
        menor.append(média - (-1.96) * desvio / math.sqrt(30))
        maior.append(média + (-1.96) * desvio / math.sqrt(30))
        mínimo.append(mntcp)
        máximo.append(mxtcp)
    f = open('rmpaicom.m', 'w')
    f.write('x = [0, 10, 50];\n')
    f.write('media = %s;\n' % repr(médias))
    f.write('menor = %s;\n' % repr(menor))
    f.write('maior = %s;\n' % repr(maior))
    f.write('minimo = %s;\n' % repr(mínimo))
    f.write('maximo = %s;\n' % repr(máximo))
    f.write("plot(x,media,';media;', x, menor, 'g;menor;', x, maior, 'g;maior;', x, minimo, 'r;minimo;', x, maximo,"
            " 'r;maximo;')\n")
    f.write("title('Remocao do diretorio pai com 30 subdiretorios')\n")
    f.write("xlabel('Tamanho Ocupado do Sistema de Arquivo (MB)')\n")
    f.write("ylabel('Tempo Gasto (ms)')\n")
    f.close()


if __name__ == '__main__':
    test_cp()
    test_rm()
    test_rm_pai_sem()
    test_rm_pai_com()
