# Laboratório 3

#### Aplicação cliente/servidor Básica usando RPC

```
Sistemas Distribuídos (ICP-367 e MAB-733)
Prof. Silvana Rossetto
Instituto de Computação/UFRJ 
```
# Descrição da tarefa
### Objetivo e Tarefa

O objetivo deste Laboratório é praticar a abstração de Chamada Remota de Procedimento (RPC).

Vamos reimplementar o **dicionário remoto** do Laboratório 2 *(com algumas alterações, descritas abaixo)*, agora usando um **middleware RPC (RPyC)**. As chaves e valores do dicionário serão strings. O dicionário deverá ser armazenado em disco para ser restaurado em uma execução futura.

O **lado servidor** da aplicação deverá oferecer as seguintes funcionalidades de um **dicionário remoto**:
- **consulta**: o usuário informará uma **chave** e receberá como resposta a **lista de valores** associados a essa chave, em ordem alfabética (lista vazia caso a entrada não exista).
- **escrita**: o usuário informará um par **chave e valor** e receberá como resposta a confirmação que a nova entrada foi inserida, ou que o novo valor foi acrescentado em uma entrada existente.
- **remoção**: o usuário informará uma **chave** e receberá como resposta a confirmação que a entrada foi removida, ou que se tratava de uma entrada inexistente.

As operações de escrita e remoção deverão ser salvas em disco de forma automática pelo servidor.

O servidor deverá ser ***multithreading***: deverá tratar cada nova conexão de cliente como um novo fluxo de execução e atender as requisições desse cliente dentro do novo fluxo de execução.
O **lado cliente** deverá oferecer uma **interface** de acesso para as funcionalidades descritas acima.

#### Disponibilize seu código
Disponibilize o código da sua aplicação em um ambiente de acesso remoto (GitHub ou GitLab) e envie o link para a professora, **usando o formulário de entrega desse laboratório**.

# Como rodar

Para executar o exemplo, basta seguir as instruções a seguir.

Primeiro, suba o lado do servidor, executando o seguinte comando no terminal:

```
python3 server.py <porta>
```

O servidor possui interface via linha de comando para a pessoa administradora. Os comandos possíveis são:
```
get: coleta um valor a partir de uma chave
get_all: coleta todos os valores
delete: deleta um valor a partir de uma chave
fim: finaliza o servidor
```

Digite **fim** como entrada para o servidor para desligar. 
Se houver clientes conectados, só irá terminar quando todos estiverem desconectados.

Depois, suba o lado do cliente, executando o seguinte comando no terminal:

```
python3 client.py <host_do_servidor> <porta_do_servidor>
```

Aceita conexões concorrentes. Sinta-se livre para usufruir disso :)

Os comandos disponíveis para o cliente são:
```
get - Consultar os valores para uma palavra.
Ex.: Para consultar a palavra "teste", digite "get teste"
set - Adicionar UM único valor por vez para uma palavra. Se a palavra não existir, será criada no dicionário
Ex.: Para adicionar o valor "valor" para a palavra "teste", digite "set teste valor"
"help" - exibe esta mensagem novamente
"fim" - encerrar o programa
```

Digite **fim** como entrada para o cliente para encerrar a conexão com o servidor.

Digite **fim** como entrada para o servidor para desligar.

