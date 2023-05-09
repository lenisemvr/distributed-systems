'''
Cliente responsável por enviar requisições ao servidor e exibir o resultado.
Pode ser executado várias vezes para testar o servidor.
Lê as mensagens do usuário até ele digitar 'fim'.
Pode consultar valores para uma palavra ou adicionar valores para uma palavra.
Para executar, digite:
python3 client.py <host> <porta-do-servidor>
'''
import socket
import sys

MESSAGE_HELP = """Este é um cliente de dicionário.
As ações disponíveis são:
get - Consultar os valores para uma palavra.\n
Para consultar a palavra "teste", digite "get teste"
set - Adicionar UM único valor por vez para uma palavra. Se a palavra não existir, será criada no dicionário
Para adicionar o valor "valor" para a palavra "teste", digite "set teste valor"
Digite "help" para exibir esta mensagem novamente
Digite "fim" para encerrar o programa\n"""

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self.connect_to_server()

    def connect_to_server(self):
        '''Cria um socket de cliente e conecta-se ao servidor'''
        # cria socket
        # Internet (IPv4 + TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # conecta-se com o servidor
        sock.connect((self.host, self.port))

        return sock
    
    def make_requests(self):
        '''Faz requisicoes ao servidor e exibe o resultado.'''
        print(MESSAGE_HELP)
        # le as mensagens do usuario ate ele digitar 'fim'
        while True:
            msg = input("Digite uma mensagem (ou 'help' para ajuda):")
            if msg == 'fim':
                break
            if msg == 'help':
                print(MESSAGE_HELP)

            # envia a mensagem do usuario para o servidor
            self.socket.send(msg.encode('utf-8'))

            #espera a resposta do servidor
            rcv = self.socket.recv(1024)
            msg = rcv.decode('utf-8')
            print(msg)
        self.socket.close()

if __name__ == '__main__':
    '''Executa o cliente'''
    if len(sys.argv) != 3:
        print(f"Chamada incorreta.\nTente: {sys.argv[0]} <host> <porta>")
        sys.exit(1)
    try:
        client = Client(sys.argv[1], int(sys.argv[2]))
    except ConnectionRefusedError:
        print("Falha na conexão com o servidor. Não é possível fazer requisições ao dicionário no momento.\nVerifique se o servidor está ativo e tente novamente...")
        sys.exit(1)
    client.make_requests()
