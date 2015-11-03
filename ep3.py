def main():
    while True:
        mensagem = input('[ep3]: ')
        palavras = mensagem.split(' ')
        if palavras[0] == 'mount':
            pass
        elif palavras[0] == 'cp':
            pass
        elif palavras[0] == 'mkdir':
            pass
        elif palavras[0] == 'rmdir':
            pass
        elif palavras[0] == 'cat':
            pass
        elif palavras[0] == 'touch':
            pass
        elif palavras[0] == 'rm':
            pass
        elif palavras[0] == 'ls':
            pass
        elif palavras[0] == 'find':
            pass
        elif palavras[0] == 'df':
            pass
        elif palavras[0] == 'umount':
            pass
        elif palavras[0] == 'sai':
            break
        else:
            print('Comando não é válido')


if __name__ == '__main__':
    main()
