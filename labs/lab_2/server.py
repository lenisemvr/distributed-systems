#servidor de echo: lado servidor
#com finalizacao do lado do servidor
#com multiplexacao do processamento (atende mais de um cliente com select)
import pprint
import socket
import select
import sys

import server.data as data
from server.processor import Processor

class Server:
    def __init__(self, port):
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
        self.socket = self.start_server()

    def start_server(self):
        '''Cria um socket de servidor e o coloca em modo de espera por conexoes
        Entrada: porta de acesso do servidor
        Saida: o socket criado'''
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

        # configura o socket para o modo nao-bloqueante
        sock.setblocking(False)

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

        #recebe dados do cliente
        body = client_socket.recv(1024) 
        if not body: # dados vazios: cliente encerrou
            print(str(addr) + '-> encerrou')
            del self.connections[client_socket] #retira o cliente da lista de conexoes ativas
            self.entries.remove(client_socket) #retira o socket do cliente das entradas do select
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
            ok = self.data.delete(key)
            if ok:
                print('Deletado com sucesso!')
        if cmd == 'fim': #solicitacao de finalizacao do servidor
            if not self.connections: #somente termina quando nao houver clientes ativos
                self.socket.close()
                sys.exit()
            else: print("ha conexoes ativas")
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
            read_list, _, _  = select.select(self.entries, [], [])
            #tratar todas as entradas prontas
            for ready in read_list:
                if ready == self.socket:  #pedido novo de conexao
                    client_socket, addr = self.accepts_connection()
                    print ('Conectado com: ', addr)
                    client_socket.setblocking(False) #configura o socket para o modo nao-bloqueante
                    # client = threading.Thread(target=self.handle_request, args=(client_socket, addr))
                    # client.start()
                    self.entries.append(client_socket) #inclui o socket do cliente nas entradas de interesse
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
