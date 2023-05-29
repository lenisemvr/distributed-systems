'''Servidor de um servico de dicionario
Responsável por receber requisicoes de clientes e processa-las, retornando o resultado.
Pode ser executado várias vezes para testar o servidor.
Para executar, digite:
python3 server.py <porta-do-servidor>'''

import sys
import rpyc

from rpyc.utils.server import ThreadedServer

import server.data as data

MESSAGE_EXECUTION_FAILED = "Falha na execução da ação, por favor verifique os argumentos"

@rpyc.service
class DictionaryServer(rpyc.Service):
    '''Classe que oferece manipulações a um dicionário local'''
    def __init__(self):
        '''Inicializa dicionário'''
        self.data = data.Data('data.json')
    
    def on_connect(self, conn):
        print('cliente conectado')
        pass

    def on_disconnect(self, conn):
        print('cliente desconectado')
        pass

    @rpyc.exposed
    def get(self, key):
        try:
            print(f"Consulta para a chave {key}")
            get_data = self.data.get(key)
            print(f"Sucesso na execução da consulta. Resultado encontrado: {get_data}\n"
                  "Resposta enviada para o cliente")
            return f"Resultado encontrado para a chave {key}: {get_data}"
        except Exception as exc:
            print(f"Erro ao executar consulta: {exc}")
            return MESSAGE_EXECUTION_FAILED
    
    @rpyc.exposed
    def set(self, key, value):
        try:
            set_type = self.data.set(key, value)
            if set_type == "old":
                print(f"Sucesso na execução da escrita. O valor {value} foi inserido na chave{key}\n"
                      "Resposta enviada para o cliente")
                return f"A chave {key} foi atualizada com o valor {value}"
            elif set_type == "new":
                print(f"Sucesso na execução da escrita. A chave {key} foi criada com o valor {value}\n"
                      "Resposta enviada para o cliente")
                return f"A chave {key} foi criada com o valor {value}"
        except Exception as exc:
            print(f"Erro ao executar escrita: {exc}")
            return MESSAGE_EXECUTION_FAILED
    
    @rpyc.exposed
    def delete(self, key):
        try:
            response = self.data.delete(key)
            print(f"Sucesso na execução da remoção. A chave {key} foi removida\n"
                      "Resposta enviada para o cliente")
            return response
        except Exception as exc:
            print(f"Erro ao executar remoção: {exc}")
            return MESSAGE_EXECUTION_FAILED

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Chamada incorreta.\nTente: {sys.argv[0]} <porta>")
        sys.exit(1)
    try: 
        dictionary_server = ThreadedServer(DictionaryServer, port=sys.argv[1])
        print("Pronto para receber conexões...")
        dictionary_server.start()
    except Exception as exc:  #erro na inicializacao do socket
        print("Erro no servidor: ", exc)
        sys.exit(1) #sai do programa
