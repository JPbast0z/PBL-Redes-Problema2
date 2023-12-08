import json
import socket
import threading
import uuid
import clock

#IP e PORT
HOST = '127.0.0.1'
PORT = int(input("Digite sua PORT"))
SINC = 'SINCRONIZAR'
mensagens_all = []
#Contatos conhecidos (Dicionario com o endereço dos usuarios conectados) - host:porta
membros_grupo = {1 : '127.0.0.1:1234', 2 : '127.0.0.1:5678', 3 : '127.0.0.1:9000'}

#Histórico de mensagens
historico_mensagens = [{'time' : 1, 'type' : 'msg', 'conteudo' : 'Olá', 'remetente' : ''}]

#Server UDP
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind((HOST, PORT))

class LamportClock:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value



#Função que recebe mens
def receber_mensagens(clock):
    while True:
        try:
            mensagem, endereco = recv_socket.recvfrom(1024)
            triagem_mensagens(mensagem)
            #print("Membro: ", endereco, "\n", "[...]", mensagem, "\n")
            clock.update()
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def triagem_mensagens(mensagem):
    mensagem = json.loads(mensagem.decode())
    if mensagem['type'] == 'msg':
        mensagem.pop('type')
        historico_mensagens.append(mensagem)
        exibir_mensagens()
    elif mensagem['type'] == 'sync':
        pass
def exibir_mensagens(clock):
    print('''
    -=-=-=-=-=-=--=--=-=-
        CHAT
    -=-=-=-=-=-=--=--=-=-
''')
    for i in historico_mensagens:
        print('TIME: ', clock, ':', i['conteudo'])

def gerar_id(): 
    return str(uuid.uuid4())

#thread para exibir mensagens

    
#Criando o objeto do relógio
clock = LamportClock()

#Thread para receber as mensagens a todo momento
thread_receber = threading.Thread(target=receber_mensagens, args=(clock))
thread_receber.start()

#Looping principal
while True:
    comando = input("Digite 'conectar' para adicionar um par conhecido ou 'enviar' para enviar mensagem: ")

    if comando == 'conectar':
        #nome_par = input("Digite o nome do par: ")
        endereco_par = input("Digite o endereço IP e porta do par (no formato IP:porta): ")
        cofre = len(membros_grupo) + 1
        membros_grupo[cofre] = str(HOST) + ':' + endereco_par
        print(f"Par {cofre} adicionado aos pares conhecidos.")
    
    elif comando == 'enviar':
        #nome_destino = input("Digite o nome do destinatário: ")
        mensagem = input("Digite a mensagem: ")
        dict_mensagem = {'time' : 1, 'type' : 'msg', 'conteudo' : mensagem, 'remetente' : str(HOST) + ':' + str(PORT)}
        
        if len(membros_grupo) != 0:
            lamport_time = clock.increment()
            for i in membros_grupo:
                if i != str(HOST) + ':' + str(PORT):
                    endereco_destino = membros_grupo[i].split(':')
                    mensagem_encode = json.dumps(dict_mensagem)
                    destino_ip = endereco_destino[0]
                    print(endereco_destino)
                    destino_porta = int(endereco_destino[1])
                    enviar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    enviar_socket.sendto(mensagem_encode.encode(), (destino_ip, destino_porta))
                    enviar_socket.close()
                    print("PASSSOUUUU")

            dict_mensagem.pop('type')
            historico_mensagens.append(dict_mensagem)
            exibir_mensagens(clock)
        else:
            print("iiiiiih")
            #print(f"O par {nome_destino} não está na lista de pares conhecidos.")