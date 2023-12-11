import json
import socket
import threading
import uuid
import os
import time
#IP e PORT
HOST = '127.0.0.1'
PORT = int(input("Digite sua PORT"))
mensagens_all = []
#Contatos conhecidos (Dicionario com o endereço dos usuarios conectados) - host:porta
membros_grupo = {1 : '127.0.0.1:1234', 2 : '127.0.0.1:5678', 3 : '127.0.0.1:9000', 4 : '127.0.0.1:1111'}

#Histórico de mensagens
historico_mensagens = []

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

def sincronizar_mensagens():
    while True:
        sinc_mensagem = {'type': 'sendMsgSync', 'host' : HOST, 'port' : PORT}
        enviar_socket(sinc_mensagem)
        time.sleep(5)

def enviar_historico_sinc(mensagem):
    
    enviar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for i in historico_mensagens:
        sinc_mensagem = {'type': 'recivMsgSync', 'data' : i}
        sinc_mensagem = json.dumps(sinc_mensagem)
        enviar_socket.sendto(sinc_mensagem.encode(), (mensagem['host'], mensagem['port']))
    enviar_socket.close()

def receber_historico_sinc(data):
    mensagem =  data['data']
    if mensagem not in historico_mensagens:
        historico_mensagens.append(mensagem)

#Função que recebe mens
def receber_mensagens(recv_socket):
    while True:
        try:
            data, endereco = recv_socket.recvfrom(1024)
            mensagem = json.loads(data.decode())
            mensagens_all.append(mensagem)
            
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

def enviar_socket(data):
    mensagem_encode = json.dumps(data)
    for i in membros_grupo:
        if membros_grupo[i] != (str(HOST) + ':' + str(PORT)):
            endereco_destino = membros_grupo[i].split(':')
            destino_ip = endereco_destino[0]
            destino_porta = int(endereco_destino[1])
            enviar_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            enviar_socket.sendto(mensagem_encode.encode(), (destino_ip, destino_porta))
            enviar_socket.close()

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

def triagem_mensagens(clock):
    while True:
        if mensagens_all:
            mensagem = mensagens_all.pop()
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
            elif mensagem['type'] == 'sendMsgSync':     
                enviar_historico_sinc(mensagem)

            elif mensagem['type'] == 'recivMsgSync':
                receber_historico_sinc(mensagem)  

def exibir_mensagens():
    os.system('cls') #windowns
    #os.system('clear') #linux
    print('''
    -=-=-=-=-=-=--=--=-=-
        CHAT
    -=-=-=-=-=-=--=--=-=-
''')
    hisorico_ordenado = sorted(historico_mensagens, key=lambda x: (x['time'], x['id']))
    for i in hisorico_ordenado:
        print('TIME: ', i['time'], ':', i['conteudo'])


def gerar_id(): 
    return str(uuid.uuid4())

def main():
    clock = LamportClock() #Criando o objeto do relógio

    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.bind((HOST, PORT))
    
    #Thread para receber as mensagens a todo momento
    thread_receber = threading.Thread(target=receber_mensagens, args=(recv_socket,))
    thread_receber.start()
    #Thread para realizar a triagem das mensagens recebidas
    thread_triagem = threading.Thread(target=triagem_mensagens, args=(clock,))
    thread_triagem.start()
    #Thread para realizar a sincronização periodica das mensagens
    thread_sinc = threading.Thread(target=sincronizar_mensagens, args=())
    thread_sinc.start()

    sincronizar_relogio(clock) #Chamada da função de sincronização do relógio
    exibir_mensagens() #Chamada da função de exibição das mensagens

    while True:
        enviar_mensagem(clock)

if __name__ == "__main__":
    main()