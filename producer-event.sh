#!/bin/bash

awslocal sqs send-message \
  --queue-url http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor.fifo \
  --message-group-id 1 \
  --message-deduplication-id 1 \
  --message-body '{"first_name": "fabio", "last_name": "nunes"}'