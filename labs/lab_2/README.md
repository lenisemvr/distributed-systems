# Laboratório 2

#### Aplicação Cliente/Servidor Básica

```
Sistemas Distribuídos (ICP-367 e MAB-733)
Prof. Silvana Rossetto
Instituto de Computação/UFRJ 
```
# Descrição da tarefa
### Introdução

O objetivo deste Laboratório é desenvolver uma aplicação distribuída para aplicar os conceitos estudados sobre arquitetura de software e arquitetura de sistema; servidores
multiplexados e concorrentes; e seguir praticando com a programação usando sockets.
A aplicação que vamos desenvolver será um **dicionário remoto** que poderá ser
consultado e alterado. As chaves e valores do dicionário serão strings. O dicionário
deverá ser armazenado em disco para ser restaurado em uma execução futura.
- Para a **consulta**, o usuário informará uma **chave** e receberá como resposta a **lista de valores** associados a essa chave, em ordem alfabética (lista vazia caso a entrada não exista).
- Para a **escrita**, o usário informará um par **chave e valor** e receberá como resposta a confirmação que a nova entrada foi inserida, ou que o novo valor foi acrescentado
em uma entrada existente.
- A **remoção** de uma entrada no dicionário somente poderá ser feita pelo **administrador**
do dicionário.

Para meu entendimento da resolução do trabalho, fiz o seguinte desenho, a partir da descrição do laboratório:
![](assets/draw-remote-dictionary.png)


### Atividade 1

**Objetivo**: Projetar a arquitetura de software da solução. A arquitetura de software
deverá conter, no mínimo, três componentes distintos: (i) acesso e persistência de dados;
(ii) processamento das requisições; e (iii) interface com o usuário.

**Roteiro**: 
1. Escolha o **estilo arquitetural** para servir de base para o desenho da arquitetura de
software.
2. Descreva os **componentes**, com suas funcionalidades (providas e usadas) e modo de conexão entre eles.

**A resolução pode ser vista [neste arquivo](activity_1.md).**

### Atividade 2

**Objetivo**: Instanciar a arquitetura de software da aplicação (definida na Atividade 1)
para uma **arquitetura de sistema cliente/servidor** de dois níveis, com um servidor e um cliente. O lado servidor abrigará o dicionário remoto, enquanto o lado cliente ficará responsável pela interface com o usuário.

**Roteiro**:
1. Defina quais componentes ficarão do lado do **cliente**.
2. Defina quais componentes ficarão do lado do **servidor**.
3. Defina o **conteúdo** e a **ordem** das mensagens que serão trocadas entre cliente e servidor, e quais **ações** cada lado deverá tomar quando receber uma mensagem.  
*Essa comunicação ficará responsável por fazer a “cola” entre os componentes instanciados em máquinas distintas.*

**A resolução pode ser vista [neste arquivo](activity_2.md).**

### Atividade 3

**Objetivo**: Implementar e avaliar a aplicação distribu ́ıda proposta, seguindo as definições da Atividade 2.

**Roteiro**:
1. Implemente o código do lado cliente e do lado servidor;
2. Modularize e documente o código de forma concisa e clara;
3. Experimente a aplicação usando diferentes casos de teste.
4. Reporte as decisões tomadas em todas as Atividades no README do repositório
do código.  
O servidor deverá ser multiplexado: capaz de receber comandos básicos da entrada padrão (inclua comandos para permitir finalizar o servidor quando não houver clientes
ativos e remover uma entrada do dicionário). **Use a função *select*.**  
O servidor deverá ser concorrente: deverá tratar cada nova conexão de cliente como um novo fluxo de execução e atender as requisições desse cliente dentro do novo
fluxo de execução. **Crie threads ou processos filhos.**

#### Disponibilize seu código
Disponibilize o código da sua aplicação em um ambiente de acesso remoto (GitHub ou GitLab) e use o formulário de entrega do laboratório para encaminhar as informações solicitadas.

# Como rodar

Para executar o exemplo, basta seguir as instruções a seguir.

Primeiro, suba o lado passivo, executando o seguinte comando no terminal:
```
make run-server
```  
OU  
```
python3 server.py
```

Depois, suba o lado ativo, executando o seguinte comando no terminal:
```
make run-client
```  
OU  
```
python3 client.py
```

Caso queira parar o exemplo, digite **fim** como entrada para o lado ativo.

# Evidências do funcionamento
![Print da execução completa](assets/images/execucao-completa-lado-a-lado.png)  
