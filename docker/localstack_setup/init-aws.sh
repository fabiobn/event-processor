#!/bin/bash

echo "===================configuring localstack==================="
LOCALSTACK_HOST=localhost
AWS_REGION=us-east-1
EVENT_PROCESSOR_LAMBDA=event-processor
EVENT_PROCESSOR_LAMBDA_ROLE=event-processor-lambda-role
EVENT_PROCESSOR_LAMBDA_ROLE_POLICY=send-message-topic-policy
EVENT_PROCESSOR_QUEUE="event-processor.fifo"
EVENT_PROCESSOR_QUEUE_DLQ="event-processor-dlq"
TOPIC_NAME_CLIENT1="event-processor-client1.fifo"
TOPIC_NAME_CLIENT2="event-processor-client2.fifo"
TOPIC_NAME_CLIENT3="event-processor-client3.fifo"

echo "===================iam create-role==================="
awslocal iam create-role \
    --role-name ${EVENT_PROCESSOR_LAMBDA_ROLE} \
    --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

echo "===================iam create-policy==================="
awslocal iam create-policy \
    --policy-name ${EVENT_PROCESSOR_LAMBDA_ROLE_POLICY} \
    --policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow","Action" : ["sns:Publish"],"Resource" : ["arn:aws:sns:$AWS_REGION:000000000000:$TOPIC_NAME_CLIENT1","arn:aws:sns:$AWS_REGION:000000000000:$TOPIC_NAME_CLIENT2","arn:aws:sns:$AWS_REGION:000000000000:$TOPIC_NAME_CLIENT3"]}]}'

echo "===================iam attach-role-policy==================="
awslocal iam attach-role-policy \
    --policy-arn arn:aws:iam::000000000000:policy/${EVENT_PROCESSOR_LAMBDA_ROLE_POLICY} \
    --role-name ${EVENT_PROCESSOR_LAMBDA_ROLE}

echo "===================sqs create-queue==================="
awslocal sqs create-queue --queue-name ${EVENT_PROCESSOR_QUEUE} --region ${AWS_REGION} --attributes '{"FifoQueue": "true", "FifoThroughputLimit": "perMessageGroupId", "ContentBasedDeduplication": "true", "DeduplicationScope": "messageGroup"}'
awslocal sqs create-queue --queue-name ${EVENT_PROCESSOR_QUEUE_DLQ} --region ${AWS_REGION}

echo "===================sns create-topic==================="
awslocal sns create-topic --name ${TOPIC_NAME_CLIENT1} --region ${AWS_REGION} --attributes '{"FifoTopic": "true", "ContentBasedDeduplication": "true"}'
awslocal sns create-topic --name ${TOPIC_NAME_CLIENT2} --region ${AWS_REGION} --attributes '{"FifoTopic": "true", "ContentBasedDeduplication": "true"}'
awslocal sns create-topic --name ${TOPIC_NAME_CLIENT3} --region ${AWS_REGION} --attributes '{"FifoTopic": "true", "ContentBasedDeduplication": "true"}'

echo "===================lambda create-function==================="
cd /var/lambda/
zip function.zip event_processor.py
awslocal lambda create-function \
    --function-name ${EVENT_PROCESSOR_LAMBDA} \
    --runtime python3.12 \
    --zip-file fileb://function.zip \
    --handler event_processor.handler \
    --dead-letter-config '{"TargetArn": "arn:aws:sqs:$AWS_REGION:000000000000:$EVENT_PROCESSOR_QUEUE_DLQ"}' \
    --role arn:aws:iam::000000000000:role/${EVENT_PROCESSOR_LAMBDA_ROLE}

echo "===================lambda create-event-source-mapping==================="
awslocal lambda create-event-source-mapping \
    --function-name ${EVENT_PROCESSOR_LAMBDA} \
    --event-source-arn arn:aws:sqs:${AWS_REGION}:000000000000:${EVENT_PROCESSOR_QUEUE}

echo "===================lambda add-permission==================="
awslocal lambda add-permission \
  --function-name ${EVENT_PROCESSOR_LAMBDA} \
  --action lambda:InvokeFunction \
  --statement-id sqs \
  --principal sqs.amazonaws.com \
  --source-arn arn:aws:sqs:${AWS_REGION}:000000000000:${EVENT_PROCESSOR_QUEUE}