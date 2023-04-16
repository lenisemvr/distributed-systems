# Exemplo basico de aplicacao distribuida usando o modelo de interacao requisicao/resposta (modo ativo/passivo)
# Uso de Programacao com Sockets, a partir do codigo fornecido em sala de aula
# LADO PASSIVO("servidor de echo") que coloca-se em modo de espera por conexoes, 
# recebe a mensagem do lado ativo e a envia de volta, 
# e repete esse procedimento ate que o lado ativo encerre a conexao. 
# Quando a conexao for encerrada, o lado passivo devera finalizar sua execucao.

import socket

# '' possibilita acessar qualquer endereco alcancavel da maquina local
HOST = ''
# porta onde chegarao as mensagens para essa aplicacao
PORTA = 5000

# cria um socket para comunicacao
# valores default: socket.AF_INET, socket.SOCK_STREAM
sock = socket.socket()

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

print("Pronto para receber conexões...")

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
# retorna um novo socket e o endereco do par conectado
novoSock, endereco = sock.accept()
print(f'Conectado com: {endereco}')

while True:
    # depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
    msg = novoSock.recv(1024) # argumento indica a qtde maxima de dados
    
    # interrompe caso nao tenha recebido mensagem
    if not msg:
        break
    
    # imprime a mensagem recebida
    message_received = str(msg,  encoding='utf-8')
    print(f'{endereco} enviou a mensagem:\n{message_received}\nVou enviar a mesma mensagem de volta.\n')
    
	# envia mensagem de resposta
    # nao eh necessario encode, pois ja esta em bytes
    novoSock.send(msg) 

# fecha o socket da conexao
novoSock.close()
print(f'Conexão com o servidor {endereco} encerrada. \o/')

# fecha o socket principal
sock.close()
print(f'Socket principal encerrado.\nAté a próxima! o/')