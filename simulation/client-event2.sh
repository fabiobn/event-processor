#!/bin/bash

echo "===================simulando recepcao cliente 2==================="
awslocal sqs receive-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor-client2.fifo \
  --region us-east-1 \
  --output json | cat