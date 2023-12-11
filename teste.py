# import threading
# mensagens_all = [43, 65]
# import time

# clock = 0
# def receber_mensagens(clock):
#     i = 0
#     while True:
#         i += 1
#         mensagens_all.append(i)
#         time.sleep(2)

# def triagem_mensagens(clock):
#     while True:
#         if mensagens_all:
#             a = mensagens_all.pop()
#             print(a)


# #Thread para receber as mensagens a todo momento
# thread_receber = threading.Thread(target=receber_mensagens, args=(clock,))
# thread_receber.start()

# print("antesss")
# thread_triagem = threading.Thread(target=triagem_mensagens, args=(clock,))
# thread_triagem.start()
# print('depoisss')


membros_grupo = {1 : '127.0.0.1:1234', 2 : '127.0.0.1:5678', 3 : '127.0.0.1:9000', 4 : '127.0.0.1:1111'}
msg = "Batata"
mensagem = ""
var = 0
var2 = 0
# for i in membros_grupo:
#     var += membros_grupo[i][:14]




for valor in membros_grupo.values():
    # Encontrar a parte da string depois do ":"
    parte_depois_do_dois_pontos = valor.split(":")[1]
    
    # Somar à variável var
    var += int(parte_depois_do_dois_pontos)

    parte_antes_do_dois_pontos = valor.split(":")[0]

    # Somar os números antes do ":" e adicionar à variável var2
    var2 += sum(int(digito) for digito in parte_antes_do_dois_pontos if digito.isdigit())

for i in msg:
    mensagem += chr (ord(i) + (var % var2))
    print(mensagem)
result = ""
for i in mensagem:
    result += chr (ord(i) - (var % var2))
    print(mensagem)
print(var)
print(var2)
print(var // var2)
print(var % var2)

print(msg)
print(len(mensagem))
print(result)