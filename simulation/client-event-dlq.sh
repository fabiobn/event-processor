#!/bin/bash

echo "===================simulando recepcao DLQ mensagens com erro==================="
awslocal sqs receive-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor-dlq.fifo \
  --region us-east-1 \
  --output json | cat