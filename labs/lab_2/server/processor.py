''' Classe responsável por processar os dados recebidos do servidor'''
# O funcionamento estah de acordo com o contrato estabelecido na atividade 2

class Processor:
    def __init__(self, data):
        self.data = data

    def process(self, data):
        '''Processa os dados recebidos do servidor'''
        data = str(data, encoding='utf-8').split(' ')
        command = data[0]
        args = data[1:]
        if command == 'get':
            if len(args) != 1:
                return "Falha na execução da ação, verifique os argumentos e a documentação"
            try:
                get_data = self.data.get(args[0])
                body = f"Resultado encontrado para a chave {args[0]}: {get_data}"
            except KeyError:
                body = "Falha na execução da ação, verifique os argumentos"
            return body
        elif command == 'set':
            if len(args) != 2:
                return "Falha na execução da ação, verifique os argumentos e a documentação"
            try:
                set_type = self.data.set(args[0], args[1])
                if set_type == "old":
                    body = f"A chave {args[0]} foi atualizada com o valor {args[1]}"
                elif set_type == "new":
                    body = f"A chave {args[0]} foi criada com o valor {args[1]}"
            except IndexError:
                body = "Falha na execução da ação, verifique os argumentos"
            return body
        else:
            return "Falha na execução da ação, verifique os argumentos"
