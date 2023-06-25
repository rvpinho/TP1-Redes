# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import os
import socket, sys
from threading import Thread

HOST = '26.141.228.32'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 2048  # tamanho do buffer para recepção dos dados

def listar_arquivos_caminho(caminho):
    sequencia = 1
    nomes_arquivos = ""
    for nome_arquivo in os.listdir(caminho):
        if os.path.isfile(os.path.join(caminho, nome_arquivo)):
            nome_com_sequencia = f"({sequencia}) {nome_arquivo}"
            nomes_arquivos += nome_com_sequencia + ", "
            sequencia += 1
    return nomes_arquivos[:-2]

def obter_conteudo_arquivo(numero_arquivo):
    
    caminho_pasta = './docs'
    arquivos_txt = [arquivo for arquivo in os.listdir(caminho_pasta) if arquivo.endswith('.txt')]
    arquivo_selecionado = arquivos_txt[numero_arquivo - 1]
    caminho_arquivo = os.path.join(caminho_pasta, arquivo_selecionado)
    
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.readlines()
        
    return conteudo

def on_new_client(clientsocket,addr):
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)
            
            if not data:
                break
            
            texto_recebido = data.decode('utf-8')
            print('Recebido do cliente {} na porta {}: {}'.format(addr[0], addr[1],texto_recebido)) 
            
            if (texto_recebido == 'connect'):
                arquivos = listar_arquivos_caminho("./docs")
                clientsocket.send('Bem Vindo ao Servidor\nEscolha o arquivo que deseja baixar: {}'.format(arquivos).encode())
                continue
            
            elif (texto_recebido == '1' or texto_recebido == '2' or texto_recebido == '3'):
                conteudo = obter_conteudo_arquivo(int(texto_recebido))
                
                print('Arquivo sendo enviado...')
                for linha in conteudo:
                    clientsocket.send(linha.encode())
                    
                clientsocket.send('fim'.encode())
                print('Arquivo enviado')
                    
                continue
            
            elif (texto_recebido == 'bye'):
                print('vai encerrar o socket do cliente {} !'.format(addr[0]))
                clientsocket.close() 
                return 
            
            else:
                clientsocket.send('O valor {} nao e refente a nenhuma opcao valida!'.format(texto_recebido).encode())
            

        except Exception as error:
            print('Erro na conexão com o cliente!!')
            return

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            
            server_socket.bind((HOST, PORT))
            print('Servidor aguardando conexões...')
            
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=on_new_client, args=(clientsocket,addr))
                t.start()   
                
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             

if __name__ == "__main__":   
    main(sys.argv[1:])