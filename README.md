# Event Processor

Implementação de case de um event processor.

## Arquitetura

![image](https://github.com/user-attachments/assets/da5a9fd1-81c8-48c0-a7ab-4b8d4efe3a39)

### Componentes

Para este case, foram utilizados os seguintes componentes:

- Localstack: para simular ambiente em cloud AWS.
  - SQS: serviço de fila para recepção de mensagens dos produtores e armazenamento de mensagens com erros em processamento(DLQ).
  - SNS: serviço de notificação pub/sub de mensagens para os clientes.
  - Lambda Function: serviço de lógica reativo a chegada da mensagem em fila para tratamento da mensagem.
  - IAM: serviço de criação de políticas e role para permissão dos serviços.
- Python: como linguagem para desenvolvimento do código da Lambda Function.
- Docker Compose: como solução em container para utilizar imagem Localstack.

## Descrição do case

De acordo com os requisitos do case, seguem algumas definições:

- Para a recepção das mensagens dos produtores, foi definida uma fila FIFO no SQS. A partir da configuração do tipo FIFO,
de message group id e sua utilização na deduplicação de mensagens, conseguimos ter um paralelismo na execução
dos eventos por group id e, em cada grupo, manter a ordem de chegada no processamento. Outra configuração foi do message
deduplication id para descartar mensagens duplicadas.
- Para difusão das mensagens para os clientes, foram definidos tópicos FIFO no SNS. A partir da configuração do tipo FIFO e
o envio da informação de message group id, conseguimos direcionar mensagens de um grupo para um determinado cliente e
manter a ordem de envio na recepção em cada um deles.
- Para o processamento reativo das mensagens que chegam na fila FIFO SQS, foi definida uma Lambda Function associada a ela.
A partir desta ligação, do tipo FIFO da fila e do envio do message group id, é possível ter uma instância da function
tratando de um tipo de mensagem.
- O serviço SNS também atuará como persistência das mensagens tratadas pelo processador de eventos. A partir dele,
um Sender pode ser criado, fazer subscrição no tópico e realizar o devido processamento relacionado a um cliente. Esta
parte não faz parte do escopo do case.
- A criação dos serviços no Localstack é feita através de um script, o qual foi mapeado via volume no arquivo docker
compose para diretório próprio utilizado na imagem Localstack na inicialização do container.
- Existem alguns scripts para simular o envio de mensagens válidas e inválidas pelos produtores, recepção das mensagens 
válidas pelos clientes, recepção de um possível tratamento de mensagens inválidas na fila DLQ e o envio de mensagens
duplicadas por um produtor.

## Como executar o case

1) Na pasta "docker", executar o comando "docker-compose up" para subir o ambiente via container Localstack.
2) Na pasta "simulation", para simular o envio de mensagens válidas por 3 produtores, execute os comandos:
   - chmod +x producer-event.sh (na primeira vez)
   - ./producer-event.sh
3) Na pasta "simulation", para simular a recepção dos clientes de cada mensagem, execute os comandos:
   - chmod +x client-event1.sh (na primeira vez)
   - ./client-event1.sh (cliente 1)
   - chmod +x client-event2.sh (na primeira vez)
   - ./client-event2.sh (cliente 2)
   - chmod +x client-event3.sh (na primeira vez)
   - ./client-event3.sh (cliente 3)
4) Na pasta "simulation", para simular o envio de mensagens inválidas por um produtor, execute os comandos:
   - chmod +x producer-event-error.sh (na primeira vez)
   - ./producer-event-error.sh
5) Na pasta "simulation", para simular a recepção de um possível tratamento da mensagem inválida na DLQ, execute os comandos:
   - chmod +x client-event-dlq.sh (na primeira vez)
   - ./client-event-dlq.sh (recepção por algum tratamento da mensagem inválida)
6) Na pasta "simulation", para simular o envio de mensagens duplicadas pelo produtor 1, execute os comandos:
   - chmod +x producer-event-duplication.sh (na primeira vez)
   - ./producer-event-duplication.sh
7) Na pasta "simulation", para simular a recepção de somente uma mensagem pelo produtor 1, execute os comandos:
   - ./client-event1.sh (retornará mensagem)
   - ./client-event1.sh (não retornará mensagem)