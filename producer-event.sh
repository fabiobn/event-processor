#!/bin/bash

awslocal sqs send-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor.fifo \
  --message-group-id 'app' \
  --message-deduplication-id '123' \
  --message-body '{"id": 123, "nome": "produto 1", "operacao": "COMPRA", "quantidade": 10, "origem": "app", "destino": "loja A"}'

awslocal sqs send-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor.fifo \
  --message-group-id 'site' \
  --message-deduplication-id '456' \
  --message-body '{"id": 456, "nome": "produto 2", "operacao": "VENDA", "quantidade": 15, "origem": "site", "destino": "loja B"}'

awslocal sqs send-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor.fifo \
  --message-group-id 'backoffice' \
  --message-deduplication-id '789' \
  --message-body '{"id": 789, "nome": "produto 3", "operacao": "COMPRA", "quantidade": 20, "origem": "backoffice", "destino": "loja C"}'