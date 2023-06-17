# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import os
import socket, sys
from threading import Thread

HOST = '127.0.0.1'  # endereço IP
PORT = 20001        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

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

def main(argv):
    try:
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((HOST, PORT))
        print("Servidor aguardando conexões...")
        
        while(True):
            
            bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE)
            mensagem = bytesAddressPair[0]
            endereco = bytesAddressPair[1]
            
            if not bytesAddressPair:
                break
            
            texto_recebido = mensagem.decode('utf-8')
            print('Recebido do cliente {} na porta {}'.format(texto_recebido, endereco)) 
            
            if (texto_recebido == 'connect'):
                arquivos = listar_arquivos_caminho("./docs")
                UDPServerSocket.sendto('Bem Vindo ao Servidor\nEscolha o arquivo que deseja baixar: {}'.format(arquivos).encode(), endereco)
                continue
            
            elif (texto_recebido == '1' or texto_recebido == '2' or texto_recebido == '3'):
                conteudo = obter_conteudo_arquivo(int(texto_recebido))
                
                print('Arquivo sendo enviado...')
                for linha in conteudo:
                    UDPServerSocket.sendto(linha.encode(), endereco)
                    
                UDPServerSocket.sendto('fim'.encode(), endereco)
                print('Arquivo enviado')
                    
                continue
            
            elif (texto_recebido == 'bye'):
                print('vai encerrar o socket do cliente {} !'.format(endereco))
                UDPServerSocket.close() 
                return 
            
            else:
                UDPServerSocket.sendto('O valor {} nao e refente a nenhuma opcao valida!'.format(texto_recebido).encode(), endereco)
            
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             

if __name__ == "__main__":   
    main(sys.argv[1:])