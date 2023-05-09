''' Classe responsável por processar os dados recebidos do servidor'''
# O funcionamento estah de acordo com o contrato estabelecido na atividade 2

class Processor:
    def __init__(self, data):
        '''Inicializa o processador com os dados disponíveis no servidor'''
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
                return f"Resultado encontrado para a chave {args[0]}: {get_data}"
            except KeyError:
                return "Falha na execução da ação, verifique os argumentos"
        elif command == 'set':
            if len(args) != 2:
                return "Falha na execução da ação, verifique os argumentos e a documentação"
            try:
                set_type = self.data.set(args[0], args[1])
                if set_type == "old":
                    return f"A chave {args[0]} foi atualizada com o valor {args[1]}"
                if set_type == "new":
                    return f"A chave {args[0]} foi criada com o valor {args[1]}"
            except IndexError:
                return "Falha na execução da ação, verifique os argumentos"
        else:
            return "Falha na execução da ação, verifique os argumentos"
