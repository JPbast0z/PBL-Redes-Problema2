import socket
import json

HOST = '127.0.0.1'
PORT = 7890
PORT2 = 1234

#Listas
ipList = [] #Lista que guarda os endereços dos novos clientes (ip dos pcs)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, PORT2))

while True:
    print("Rodando server...")
    #RECEBENDO MENSAGEM
    mensagem, ip_outher_client = client_socket.recvfrom(1024)
    mensagem = mensagem.decode()
    print(mensagem)

    #ENVIANDO MENSAGEM
    envio_mensagem = input("Digite sua mensagem: ")
    client_socket.sendto(envio_mensagem.encode(), (HOST, PORT))