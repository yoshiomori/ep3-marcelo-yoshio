import sys
import time

tamanho_cabeçalho = 14  # O cabeçalho tem 14 blocos
tamanho_bloco = 4000  # O tamanho de um bloco é 4000kB
tamanho_unidade = 100000000  # O tamanho máximo da unidade simulada é 100MB
unidade_simulada = None
nome_arquivo = None
mapa_bit = None
fat = None


# Função que calcula o numero_blocos
def numero_blocos():
    return int(tamanho_unidade / tamanho_bloco)


# Função que calcula o tamanho da tabela fat
def tamanho_fat():
    return numero_blocos() - tamanho_cabeçalho


# Função que calcula a posição na unidade simulada dado o índice do bloco
def posição_unidade_por_índice_bloco(índice):
    return índice * tamanho_bloco


# Função que retorna a posição da raíz
def posição_raíz():
    return posição_unidade_por_índice_bloco(tamanho_cabeçalho)  # Vai para a primeira posição depois do cabeçalho


# Carrega o mapa de bits e a tabela fat do arquivo para a memória
def carregar_dados():
    global mapa_bits, fat
    mapa_bits = int.from_bytes(unidade_simulada.read(2), sys.byteorder)

    # 25000 blocos em 100MB e o cabeçalho usa 14 blocos
    fat = [int.from_bytes(unidade_simulada.read(2), sys.byteorder) for _ in range(tamanho_fat())]


# Escreve um arquivo com um mapa de bits, uma tabela fat e o diretório raiz com seus valores iniciais
def criar_unidade():
    # Criando um mapa de bits com todas as entradas 1 exceto pelo primero bit, que está associado ao bloco da raíz
    unidade_simulada.write(int(65534).to_bytes(2, sys.byteorder))

    # Criando a tabela fat com (25000 - 14) entradas.
    # Há 25000 blocos em 100MB e o cabeçalho usa 14 blocos
    unidade_simulada.write(int(-1).to_bytes(2, sys.byteorder, signed=True))  # trata da entrada da raíz
    for _ in range(numero_blocos() - tamanho_cabeçalho - 1):  # Trata das outras entradas
        unidade_simulada.write(int(42).to_bytes(2, sys.byteorder))  # 42 é um número qualquer

    # Vai para a raíz
    unidade_simulada.seek(posição_raíz())

    # Criando o bloco do diretório raiz
    unidade_simulada.write(int(0).to_bytes(2, sys.byteorder))  # magic number
    unidade_simulada.write('/'.zfill(255).encode('unicode_escape'))  # nome do diretório
    unidade_simulada.write(time.asctime().encode('unicode_escape'))  # Instante criado
    unidade_simulada.write(time.asctime().encode('unicode_escape'))  # Instante modificado
    unidade_simulada.write(time.asctime().encode('unicode_escape'))  # Instante acessado


# Função responsável por criar e montar unidade de arquivo
def mount(argumento):
    global nome_arquivo, unidade_simulada
    nome_arquivo = argumento
    try:
        unidade_simulada = open(nome_arquivo, 'r+b')
    except FileNotFoundError:
        unidade_simulada = open(nome_arquivo, 'w+b')
        criar_unidade()
        print('%s foi criada com sucesso' % nome_arquivo)
    carregar_dados()
    print('%s foi montada com sucesso' % nome_arquivo)


def umount():
    unidade_simulada.close()
    print('%s foi desmontada com sucesso' % nome_arquivo)


def main():
    estado = 'umount'
    while True:
        mensagem = input('[ep3]: ')
        comando, sep, argumentos = mensagem.partition(' ')
        if comando == 'mount' and estado == 'umount':
            # Verificando se o argumento do comando é válido
            if not argumentos:
                print('Uso: mount <nome do arquivo>')
            else:
                mount(argumentos)
                estado = 'mount'
        elif comando == 'cp' and estado == 'mount':
            pass
        elif comando == 'mkdir' and estado == 'mount':
            pass
        elif comando == 'rmdir' and estado == 'mount':
            pass
        elif comando == 'cat' and estado == 'mount':
            pass
        elif comando == 'touch' and estado == 'mount':
            pass
        elif comando == 'rm' and estado == 'mount':
            pass
        elif comando == 'ls' and estado == 'mount':
            pass
        elif comando == 'find' and estado == 'mount':
            pass
        elif comando == 'df' and estado == 'mount':
            pass
        elif comando == 'umount' and estado == 'mount':
            umount()
            estado = 'umount'
            pass
        elif comando == 'sai' and estado == 'umount':
            break
        elif comando == 'sai' and estado == 'mount':
            umount()
            break
        else:
            print('%s não é um comando válido' % comando)


if __name__ == '__main__':
    main()
