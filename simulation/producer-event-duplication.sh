#!/bin/bash

echo "===================simulando envio mensagem produtor 1==================="
awslocal sqs send-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor.fifo \
  --message-group-id 'app' \
  --message-deduplication-id '123' \
  --message-body '{"id": 123, "nome": "produto 1", "operacao": "COMPRA", "quantidade": 10, "origem": "app", "destino": "loja A"}'

echo "===================simulando envio mensagem duplicada produtor 1==================="
awslocal sqs send-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor.fifo \
  --message-group-id 'app' \
  --message-deduplication-id '123' \
  --message-body '{"id": 123, "nome": "produto 1", "operacao": "COMPRA", "quantidade": 10, "origem": "app", "destino": "loja A"}'