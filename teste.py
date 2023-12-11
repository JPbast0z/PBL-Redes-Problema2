import threading
mensagens_all = [43, 65]
import time

clock = 0
def receber_mensagens(clock):
    i = 0
    while True:
        i += 1
        mensagens_all.append(i)
        time.sleep(2)

def triagem_mensagens(clock):
    while True:
        if mensagens_all:
            a = mensagens_all.pop()
            print(a)


#Thread para receber as mensagens a todo momento
thread_receber = threading.Thread(target=receber_mensagens, args=(clock,))
thread_receber.start()

print("antesss")
thread_triagem = threading.Thread(target=triagem_mensagens, args=(clock,))
thread_triagem.start()
print('depoisss')
