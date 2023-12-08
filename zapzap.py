import json
import socket
import threading
import uuid
#import clock

#IP e PORT
HOST = '127.0.0.1'
PORT = int(input("Digite sua PORT"))
SINC = 'SINCRONIZAR'
mensagens_all = []
#Contatos conhecidos (Dicionario com o endereço dos usuarios conectados) - host:porta
membros_grupo = {1 : '127.0.0.1:1234', 2 : '127.0.0.1:5678', 3 : '127.0.0.1:9000', 4 : '127.0.0.1:1111'}

#Histórico de mensagens
historico_mensagens = [{'time' : 0, 'type' : 'msg', 'conteudo' : 'Olá', 'remetente' : '', 'id' : 'idTeste456156'}]

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

def sincronizar_relogio(clock):
    sinc_mensagem = {'type': 'clockSync', 'clock': clock.value, 'host' : HOST, 'port' : PORT}
    enviar_socket(sinc_mensagem)

#Função que recebe mens
def receber_mensagens(clock):
    while True:
        try:
            print('1')
            data, endereco = recv_socket.recvfrom(1024)
            print(2)
            triagem_mensagens(data, clock)
            #print("Membro: ", endereco, "\n", "[...]", mensagem, "\n")
            
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def enviar_socket(data):
    mensagem_encode = json.dumps(data)
    for i in membros_grupo:
        if membros_grupo[i] != (str(HOST) + ':' + str(PORT)):
            endereco_destino = membros_grupo[i].split(':')
            destino_ip = endereco_destino[0]
            print(endereco_destino)
            destino_porta = int(endereco_destino[1])
            enviar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            enviar_socket.sendto(mensagem_encode.encode(), (destino_ip, destino_porta))
            enviar_socket.close()
            print("PASSSOUUUU")

def enviar_mensagem(clock):
    
        #nome_destino = input("Digite o nome do destinatário: ")
        mensagem = input("Digite a mensagem: ")
        clock.increment()
        id = gerar_id()
        dict_mensagem = {'time' : clock.value, 'type' : 'msg', 'conteudo' : mensagem, 'remetente' : str(HOST) + ':' + str(PORT), 'id' : id}
            
        enviar_socket(dict_mensagem)

        dict_mensagem.pop('type')
        historico_mensagens.append(dict_mensagem)
        exibir_mensagens()

def triagem_mensagens(dados, clock):
    mensagem = json.loads(dados.decode())
    if mensagem['type'] == 'msg':
        mensagem.pop('type')
        clock.update(mensagem['time'])
        historico_mensagens.append(mensagem)
        exibir_mensagens()
    elif mensagem['type'] == 'clockSync':
        clock.update(mensagem['clock'])
        sinc_mensagem = {'type': 'updateClock', 'clock': clock.value}
        sinc_mensagem = json.dumps(sinc_mensagem)
        enviar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        enviar_socket.sendto(sinc_mensagem.encode(), (mensagem['host'], mensagem['port']))
        enviar_socket.close()
    elif mensagem['type'] == 'updateClock':
        clock.update(mensagem['clock'])
        print('02 - ',HOST, ' : ', PORT, ' -> ', clock.value)
        

def exibir_mensagens():
    print('''
    -=-=-=-=-=-=--=--=-=-
        CHAT
    -=-=-=-=-=-=--=--=-=-
''')
    for i in historico_mensagens:
        print('TIME: ', i['time'], ':', i['conteudo'])

def gerar_id(): 
    return str(uuid.uuid4())

#thread para exibir mensagens

    
#Criando o objeto do relógio
clock = LamportClock()

#Thread para receber as mensagens a todo momento
thread_receber = threading.Thread(target=receber_mensagens, args=(clock,))
thread_receber.start()
sincronizar_relogio(clock)
print(HOST, ' : ', PORT, ' -> ', clock.value)
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
        enviar_mensagem(clock)