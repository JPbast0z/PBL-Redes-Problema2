import socket

# Configurar o endereço IP e a porta do nó B
host_b, host_a = '127.0.0.1', '127.0.0.1'
port_b = 54321
port_a = 12345

# Criar um socket
socket_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_b.bind((host_b, port_b))

while True:
    data, _ = socket_b.recvfrom(1024)
    print(f"Nó A diz: {data.decode()}")
    reply = input("Digite uma resposta para enviar ao nó A: ")
    socket_b.sendto(reply.encode(), (host_a, port_a))
