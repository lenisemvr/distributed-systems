# Exemplo basico de aplicacao distribuida usando o modelo de interacao requisicao/resposta (modo ativo/passivo)
# Uso de Programacao com Sockets, a partir do codigo fornecido em sala de aula
# LADO ATIVO, que conecta-se com o "servidor de echo" (lado passivo), 
# envia uma mensagem digitada pelo usuario, aguarda e imprime a mensagem recebida de volta
# A string fim deve ser usada como comando para o usuario indicar que 
# nao deseja mais enviar mensagens para o servidor de echo. 
# Quando esse comando for digitado pelo usuario, a conexao devera ser fechada e a aplicacao encerrada.
# Nesse caso, nao eh necessario enviar o comando para o lado passivo.

import socket

# maquina onde esta o par passivo
HOST = 'localhost'
# porta que o par passivo esta escutando
PORTA = 5000

# criacao do socket
# default: socket.AF_INET, socket.SOCK_STREAM
sock = socket.socket()

# conecta-se com o "servidor de echo" (lado passivo)
sock.connect((HOST, PORTA))

# loop para troca de mensagens, conforme indicado no roteiro
while True:
    message = input("Por favor, insira a mensagem que deseja enviar...\n")

    # confere se a mensagem eh o comando de termino, se for a string fim interrompe a execucao
    if message == "fim":
        break
    
    # envia a mensagem recebida para o par conectado
    sock.send(message.encode())
    
    #espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
    # argumento indica a qtde maxima de bytes da mensagem
    msg_r = sock.recv(1024)

    # imprime a mensagem recebida de volta
    received_message = str(msg_r, encoding='utf-8')
    print(f'Recebi a mensagem:\n{received_message}\n')

# encerra a conexao
print('Fluxo interrompido. Conexão encerrada! :)')
sock.close()