import socket

# Configurar o endereço IP e a porta do nó A
host_a, host_b = '127.0.0.1', '127.0.0.1'
port_a = 12345
port_b = 54321

# Criar um socket
socket_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_a.bind((host_a, port_a))

while True:
    message = input("Digite uma mensagem para enviar ao nó B: ")
    socket_a.sendto(message.encode(), (host_b, port_b))
    data, _ = socket_a.recvfrom(1024)
    print(f"Nó B diz: {data.decode()}")