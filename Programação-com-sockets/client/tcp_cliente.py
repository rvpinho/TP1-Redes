# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket, sys
import os

HOST = '26.97.191.32'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 4096  # tamanho do buffer para recepção dos dados

def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.connect((HOST, PORT))
            
            server.send('connect'.encode())
            data = server.recv(BUFFER_SIZE)
            print(data.decode('utf-8'))
            
            while True:
                texto = input("Digite o número do arquivo ou bye para sair: ")
                
                if(texto == '1' or texto == '2' or texto == '3'):
                    server.send(texto.encode())
                    
                    caminho_pasta = './docs'
                    nome_arquivo = 'arquivoBaixado.txt'
                    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                    
                    print('Arquivo sendo baixado...')
                    with open(caminho_arquivo, 'w') as arquivo:
                        while True:
                            data = server.recv(BUFFER_SIZE)
                            linha = data.decode('utf-8', 'ignore')
                            
                            if linha.strip() == 'fim':
                                break
                            
                            arquivo.write(str(linha))   
                    print("Arquivo baixado com sucesso.")
                
                elif (texto == 'bye'):
                    print('vai encerrar o socket cliente!')
                    server.send(texto.encode())
                    server.close()
                    break
                
                else:                
                    server.send(texto.encode())
                    data = server.recv(BUFFER_SIZE)
                    texto_recebido = data.decode('utf-8') 
                    print('Recebido do servidor:', texto_recebido)
                
    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])