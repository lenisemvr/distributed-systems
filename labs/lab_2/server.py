'''Servidor de um servico de dicionario
Responsável por receber requisicoes de clientes e processa-las, retornando o resultado.
Pode ser executado várias vezes para testar o servidor.
Para executar, digite:
python3 server.py <porta-do-servidor>'''
import pprint
import socket
import select
import sys
import multiprocessing
import threading

import server.data as data
from server.processor import Processor

class Server:
    def __init__(self, port):
        '''Inicializa o servidor com a porta do servidor'''
        self.host = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
        self.port = port
        # inicializa classe Data, carregando o arquivo de dados
        self.data = data.Data('data.json')
        # inicializa classe Processor, que ira processar as requisicoes
        self.processor = Processor(self.data)
        #define a lista de I/O de interesse (jah inclui a entrada padrao)
        self.entries = [sys.stdin]
        #armazena as conexoes ativas
        self.connections = {}
        self.clients = []
        self.socket = self.start_server()
        self.lock = threading.Lock()

    def start_server(self):
        '''Cria um socket de servidor e o coloca em modo de espera por conexoes'''
        # cria o socket
        # Internet( IPv4 + TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # permite que o endereco/porta possam ser reutilizados e evita o Errno 48
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # vincula a localizacao do servidor
        sock.bind((self.host, self.port))

        # coloca-se em modo de espera por conexoes
        sock.listen(5)
        print(f"Ouvindo na porta {self.port}...")

        # precisei comentar essa linha para funcionar
        # sock.setblocking(False)

        # inclui o socket principal na lista de entradas de interesse
        self.entries.append(sock)

        return sock

    def accepts_connection(self):
        '''Aceita o pedido de conexao de um cliente
        Entrada: o socket do servidor
        Saida: o novo socket da conexao e o endereco do cliente'''

        # estabelece conexao com o proximo cliente
        client_socket, addr = self.socket.accept()

        # registra a nova conexao
        self.connections[client_socket] = addr

        return client_socket, addr

    def handle_request(self, client_socket, addr):
        '''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
        Entrada: socket da conexao e endereco do cliente
        Saida: '''

        while True:
            #recebe dados do cliente
            body = client_socket.recv(1024) 
            if not body: # dados vazios: cliente encerrou
                print(str(addr) + '-> encerrou')
                client_socket.close() # encerra a conexao com o cliente
                return
            body = self.processor.process(body)
            # envia dados para o cliente
            print(f'{str(addr)} vai receber o valor: {body}')
            client_socket.sendall(bytes(body, encoding='utf-8'))
    
    def admin_cmd(self):
        '''Trata comandos do admin (entrada padrao)'''
        cmd = input()
        if cmd == 'get':
            key = input('Insira a chave que deseja coletar: ')
            print(self.data.get(key))
        if cmd == 'get_all':
            pprint.pprint(self.data.get_all())
        if cmd == 'delete':
            key = input('Insira a chave que deseja deletar: ')
            self.data.delete(key)
        if cmd == 'fim': #solicitacao de finalizacao do servidor
            print( "Conferindo se há processos a terminarem...")
            for c in self.clients:
                if c.is_alive():
                    print("Ainda há processos a terminarem...")
                    c.join()
            print("Todos os processos terminaram!")
            print("Finalizando servidor...")
            self.socket.close()
            sys.exit()
        elif cmd == 'help':
            print('Comandos disponíveis:')
            print('get: coleta um valor a partir de uma chave')
            print('get_all: coleta todos os valores')
            print('delete: deleta um valor a partir de uma chave')
            print('fim: finaliza o servidor')

    def run(self):
        '''Inicializa e implementa o loop principal (infinito) do servidor'''
        while True:
            #espera por qualquer entrada de interesse
            ready_list, _, _  = select.select(self.entries, [], [])
            #tratar todas as entradas prontas
            for ready in ready_list:
                if ready == self.socket:  #pedido novo de conexao
                    client_socket, addr = self.accepts_connection()
                    print ('Conectado com: ', addr)
                    client = multiprocessing.Process(target=self.handle_request, args=(client_socket, addr))
                    client.start()
                    self.clients.append(client)
                    # client_socket.setblocking(False) #configura o socket para o modo nao-bloqueante
                    # client = threading.Thread(target=self.handle_request, args=(client_socket, addr))
                    # client.start()
                    # self.entries.append(client_socket) #inclui o socket do cliente nas entradas de interesse
                elif ready == sys.stdin: #entrada padrao
                    self.admin_cmd()
                else:
                    self.handle_request(ready, self.connections[ready])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Chamada incorreta.\nTente: {sys.argv[0]} <porta>")
        sys.exit(1)
    try:
        server = Server(int(sys.argv[1]))
        print("Pronto para receber conexoes...\nTambém é possível inserir comandos pelo terminal. Para mais informações, digite 'help'")
        server.run()
    except Exception as exc:  #erro na inicializacao do socket
        print("Erro no servidor: ", exc)
        sys.exit(1) #sai do programa
