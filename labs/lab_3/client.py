'''
Cliente responsável por enviar requisições ao servidor e exibir o resultado.
Pode ser executado várias vezes para testar o servidor.
Lê as mensagens do usuário até ele digitar 'fim'.
Pode consultar valores para uma palavra ou adicionar valores para uma palavra.
Para executar, digite:
python3 client.py <host> <porta-do-servidor>
'''

import rpyc #modulo que oferece suporte a abstracao de RPC
import sys

MESSAGE_HELP = """Este é um cliente de dicionário.
As ações disponíveis são:
get - Consultar os valores para uma palavra.
Digite "get" e siga as instruções do prompt
set - Adicionar UM único valor por vez para uma palavra. Se a palavra não existir, será criada no dicionário.
Digite "set" e siga as instruções do prompt
delete - Apagar uma palavra. Se a palavra não existir no dicionário, o servidor irá informar.
Digite "delete" e siga as instruções do prompt
Digite "help" para exibir esta mensagem novamente
Digite "fim" para encerrar o programa\n"""

MESSAGE_WRONG_ARGUMENTS = "Número de argumentos inválido, por favor verifique os argumentos e a documentação"

class Client:
    def __init__(self, host, port):
        '''Inicializa o cliente com o host e a porta do servidor'''
        self.host = str(host)
        self.port = port
        self.conn = self.connect_to_server()

    def connect_to_server(self):
        '''Conecta-se ao servidor usando RPyC'''
        conn = rpyc.connect(self.host, self.port)
        type_conn = type(conn.root)
        service_name = conn.root.get_service_name()
        # exibe o nome da classe (servico) oferecido e mostra que conn.root eh um stub de cliente
        print(f'Conexão criada!\n O serviço oferecido é {service_name} e o tipo de conexão é {type_conn}\n')

        return conn
            
    def make_requests(self):
        '''Faz requisicoes ao servidor e exibe o resultado.'''
        print(MESSAGE_HELP)
        # le as mensagens do usuario ate ele digitar 'fim'
        while True:
            command = input("Digite o comando que deseja executar (ou 'help' para ajuda):")
            if command == 'fim':
                print("Encerrando cliente... Tchau o/")
                self.conn.close()
                break
            elif command == 'help':
                print(MESSAGE_HELP)
            elif command == 'get':
                input_raw = input("Digite a chave que deseja consultar:\n")
                args = input_raw.split()
                if len(args) != 1:
                    print(MESSAGE_WRONG_ARGUMENTS)
                    continue
                response = self.conn.root.get(args[0])
                print(response)
            elif command == 'set':
                input_raw = input("Digite a chave e o valor para inserção:\n")
                args = input_raw.split()
                if len(args) != 2:
                    print(MESSAGE_WRONG_ARGUMENTS)
                    continue
                response = self.conn.root.set(args[0], args[1])
                print(response)
            elif command == 'delete':
                input_raw = input("Digite a chave que deseja apagar:\n")
                args = input_raw.split()
                if len(args) != 1:
                    print(MESSAGE_WRONG_ARGUMENTS)
                    continue
                response = self.conn.root.delete(args[0])
                print(response)

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
