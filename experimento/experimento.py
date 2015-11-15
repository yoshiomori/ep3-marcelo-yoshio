import ep3
import os
import sys
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


def experimento(nome_sistema):
    tempo_cp = {'arquivo1MB': 0, 'arquivo10MB': 0, 'arquivo30MB': 0}
    tempo_rm = {'arquivo1MB': 0, 'arquivo10MB': 0, 'arquivo30MB': 0}
    ep3.mount(nome_sistema)
    for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
        try:
            tempo_cp[nome_arquivo] = tempo_op(ep3.cp, (nome_arquivo, '/'))
        except MemoryError:
            pass
    for nome_arquivo in ['arquivo1MB', 'arquivo10MB', 'arquivo30MB']:
        tempo_rm[nome_arquivo] = tempo_op(ep3.rm, ('/' + nome_arquivo,))
    tempo_rm_pai_sem_arquivos = tempo_op(ep3.rmdir, ('/pai_sem',))
    tempo_rm_pai_com_arquivos = tempo_op(ep3.rmdir, ('/pai_com',))
    ep3.umount()
    return tempo_cp.values(), tempo_rm.values(), tempo_rm_pai_sem_arquivos, tempo_rm_pai_com_arquivos


def cp(nome_origem, nome_destino):
    origem = open(nome_origem, 'rb')
    destino = open(nome_destino, 'wb')
    destino.write(origem.read())
    destino.close()
    origem.close()


def esoma(a, b, c, d, e, f, g, h):
    return [i + j for i, j in zip(a, e)], [i + j for i, j in zip(b, f)], c + g, d + h


def emin(a, b, c, d, e, f, g, h):
    return [min(i, j) for i, j in zip(a, e)], [min(i, j) for i, j in zip(b, f)], min(c, g), min(d, h)


def emax(a, b, c, d, e, f, g, h):
    return [max(i, j) for i, j in zip(a, e)], [max(i, j) for i, j in zip(b, f)], max(c, g), max(d, h)


def main():
    # Soma total
    stcp = [0, 0, 0]
    strm = [0, 0, 0]
    strmps = 0
    strmpc = 0

    # Maximo
    mxtcp = [float('-inf'), float('-inf'), float('-inf')]
    mxtrm = [float('-inf'), float('-inf'), float('-inf')]
    mxtrmps = float('-inf')
    mxtrmpc = float('-inf')

    # Mínimo
    mntcp = [float('inf'), float('inf'), float('inf')]
    mntrm = [float('inf'), float('inf'), float('inf')]
    mntrmps = float('inf')
    mntrmpc = float('inf')

    cp('arquivos/arquivo1MB', 'arquivo1MB')
    cp('arquivos/arquivo10MB', 'arquivo10MB')
    cp('arquivos/arquivo30MB', 'arquivo30MB')
    for i in range(30):
        print('iteração %d' % i)
        cp('arquivos/' + sys.argv[1], sys.argv[1])
        a, b, c, d = experimento(sys.argv[1])
        stcp, strm, strmps, strmpc = esoma(a, b, c, d, stcp, strm, strmps, strmpc)
        mntcp, mntrm, mntrmps, mntrmpc = emin(a, b, c, d, mntcp, mntrm, mntrmps, mntrmpc)
        mxtcp, mxtrm, mxtrmps, mxtrmpc = emax(a, b, c, d, mxtcp, mxtrm, mxtrmps, mxtrmpc)
        os.remove(sys.argv[1])
    os.remove('arquivo1MB')
    os.remove('arquivo10MB')
    os.remove('arquivo30MB')
    file = open('experimento' + sys.argv[1], 'w')
    file.write('soma dos tempos de cp: ' + str(stcp) + '\n')
    file.write('soma dos tempos de rm: ' + str(strm) + '\n')
    file.write('soma dos tempos de rm do diretório pai sem arquivos: ' + str(strmps) + '\n')
    file.write('soma dos tempos de rm do diretório pai com arquivos: ' + str(strmpc) + '\n')

    file.write('min dos tempos de cp: ' + str(mntcp) + '\n')
    file.write('min dos tempos de rm: ' + str(mntrm) + '\n')
    file.write('min dos tempos de rm do diretório pai sem arquivos: ' + str(mntrmps) + '\n')
    file.write('min dos tempos de rm do diretório pai com arquivos: ' + str(mntrmpc) + '\n')

    file.write('max dos tempos de cp: ' + str(mxtcp) + '\n')
    file.write('max dos tempos de rm: ' + str(mxtrm) + '\n')
    file.write('max dos tempos de rm do diretório pai sem arquivos: ' + str(mxtrmps) + '\n')
    file.write('max dos tempos de rm do diretório pai com arquivos: ' + str(mxtrmpc) + '\n')
    file.close()


if __name__ == '__main__':
    main()
