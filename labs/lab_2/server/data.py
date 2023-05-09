# create a Data class to store and get key and values on a file concurrent safe
# the file will be opened in the constructor and closed in the destructor
# the file will be a a json with the following format:
# { key: [value1, value2, ...], ... }

import json
from threading import Lock

class Data:
    def __init__(self, filename):
        '''Constructor'''
        '''Abre o arquivo e carrega o json para o dicionario'''
        self.filename = filename
        self.file = open(filename, 'r+')
        self.lock = Lock()

    def __del__(self):
        '''Destructor'''
        '''Fecha o arquivo ao final da execução'''
        self.file.close()

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
        json.dump(data, self.file, indent=4)
        self.lock.release()
        return set_type

    def delete(self, key):
        '''Deleta um valor do dicionário'''
        self.lock.acquire()
        self.file.seek(0)
        data = json.load(self.file)
        if key in data:
            del data[key]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        self.lock.release()