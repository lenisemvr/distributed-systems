'''Módulo responsável por gerenciar os dados do dicionário'''
# O funcionamento estah de acordo com o contrato estabelecido na atividade 2

import json
import multiprocessing


class Data:
    def __init__(self, filename):
        '''Constructor'''
        '''Abre o arquivo e carrega o json para o dicionario'''
        self.filename = filename
        self.file = self.open(filename)
        self.lock = multiprocessing.Lock()

    def __del__(self):
        '''Destructor'''
        '''Fecha o arquivo ao final da execução'''
        self.file.close()
    
    def open(self, filename):
        '''Abre o arquivo e retorna o json
        Se o arquivo não existir, cria um novo'''
        try:
            file = open(filename, 'r+')
        except FileNotFoundError:
            file = open(filename, 'w+')
        return file
    
    def save(self):
        '''Salva o dicionario no arquivo'''
        self.lock.acquire()
        self.file.seek(0)
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            print("Dicionário está vazio. Por favor, insira um valor via cliente.")
            data = {}
        self.file.seek(0)
        json.dump(data, self.file)
        self.file.truncate()
        self.lock.release()


    def get(self, key):
        '''Retorna o valor da chave passada como argumento'''
        self.lock.acquire()
        self.file.seek(0)
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            print("Dicionário está vazio. Por favor, insira um valor via cliente.")
            data = {}
        self.lock.release()
        # if the key is not in the file, return an empty list
        if key not in data:
            return []
        sorted_data = sorted(data[key])
        return sorted_data
    
    def get_all(self):
        '''Retorna todos os valores do dicionário'''
        self.lock.acquire()
        self.file.seek(0)
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            print("Dicionário está vazio. Por favor, insira um valor via cliente.")
            data = {}
        self.lock.release()
        return data

    def set(self, key, value):
        '''Insere um valor no dicionário'''
        set_type = ""
        self.lock.acquire()
        self.file.seek(0)
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            print("Dicionário está vazio... Inserindo novo valor")
            data = {}
        if key in data:
            data[key].append(value)
            set_type = "old"
        else:
            data[key] = [value]
            set_type = "new"
        self.file.seek(0)
        json.dump(data, self.file)
        self.file.truncate()
        self.lock.release()
        return set_type

    def delete(self, key):
        '''Deleta uma chave e seus valores'''
        self.lock.acquire()
        self.file.seek(0)
        try:
            data = json.load(self.file)
            if key in data:
                del data[key]
                response = f"Chave {key} deletada com sucesso"
            else:
                response = "Chave não está presente no dicionário. Por favor, verifique e tente outra"
            self.file.seek(0)
            json.dump(data, self.file)
            self.file.truncate()
            self.lock.release()
            return response
        except json.decoder.JSONDecodeError:
            return "Dicionário está vazio... Não há o que deletar"
        except:
            raise Exception
    