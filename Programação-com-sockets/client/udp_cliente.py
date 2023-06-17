# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import os
import socket, sys

HOST = '127.0.0.1'  # endereço IP
PORT = 20001        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 
    try:
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as UDPClientSocket:
            
            UDPClientSocket.sendto('connect'.encode(), (HOST, PORT))
            data = UDPClientSocket.recvfrom(BUFFER_SIZE)
            print(data[0].decode('utf-8'))
            
            while True:
                
                texto = input("Digite o número do arquivo ou bye para sair: ")
                
                if(texto == '1' or texto == '2' or texto == '3'):
                    UDPClientSocket.sendto(texto.encode(), (HOST, PORT))
                    
                    caminho_pasta = './docs'
                    nome_arquivo = 'arquivoBaixado.txt'
                    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                    
                    print('Arquivo sendo baixado...')
                    with open(caminho_arquivo, 'w') as arquivo:
                        while True:
                            data = UDPClientSocket.recvfrom(BUFFER_SIZE)
                            linha = data[0].decode('utf-8', 'ignore')
                            
                            if linha.strip() == 'fim':
                                break
                            
                            arquivo.write(str(linha) + '\n')
                            
                    print("Arquivo baixado com sucesso.")
                
                elif (texto == 'bye'):
                    print('vai encerrar o socket cliente!')
                    UDPClientSocket.sendto(texto.encode(), (HOST, PORT))
                    UDPClientSocket.close()
                    break
                
                else:                
                    UDPClientSocket.sendto(texto.encode(), (HOST, PORT))
                    data = UDPClientSocket.recvfrom(BUFFER_SIZE)
                    texto_recebido = data[0].decode('utf-8') 
                    print('Recebido do servidor:', texto_recebido)
                

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])