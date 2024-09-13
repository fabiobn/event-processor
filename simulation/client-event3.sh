#!/bin/bash

echo "===================simulando recepcao cliente 3==================="
awslocal sqs receive-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor-client3.fifo \
  --region us-east-1 \
  --output json | cat