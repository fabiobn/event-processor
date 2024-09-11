import json

TOPIC_ARN1="arn:aws:sns:us-east-1:000000000000:event-processor-client1.fifo"
TOPIC_ARN2="arn:aws:sns:us-east-1:000000000000:event-processor-client2.fifo"
TOPIC_ARN3="arn:aws:sns:us-east-1:000000000000:event-processor-client3.fifo"

SQS_QUEUE_DLQ="http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/event-processor-dlq"

class SNSDeliveryService:

    def __init__(self, sns_client):
        self.sns_client = sns_client

    def publish_message(self, message):
        try:
            print(f"Sending message to SNS")
            print(f"Message to send to SNS: {json.dumps(message, indent=2)}")
            topic_to_send = ""
            if message.destino == "loja A":
                topic_to_send = TOPIC_ARN1
            elif message.destino == "loja B":
                topic_to_send = TOPIC_ARN2
            else:
                topic_to_send = TOPIC_ARN3
            print(f"Topic: {topic_to_send}")
            # publish message to sns
            snsResponse = self.sns_client.publish(
                TargetArn=topic_to_send,
                Message=json.dumps(message, indent=2),
                Subject='TESTE',
                MessageGroupId='1',
                MessageDeduplicationId='1'
            )
            print(f"Message sent to SNS: {json.dumps(message, indent=2)}")
        except Exception as error:
            print("An exception occurred:", error)
            raise error

class SQSDeliveryService:

    def __init__(self, sqs_client):
        self.sqs_client = sqs_client

    def send_message(self, message):
        try:
            print(f"Sending message to SQS")
            print(f"Message to send to SQS: {json.dumps(message, indent=2)}")
            print(f"SQS: {SQS_QUEUE_DLQ}")
            # publish message to sns
            sqsResponse = self.sqs_client.send_message(
                QueueUrl=SQS_QUEUE_DLQ,
                MessageBody=json.dumps(message, indent=2)
            )
            print(f"Message sent to SQS: {json.dumps(message, indent=2)}")
        except Exception as error:
            print("An exception occurred:", error)
            raise error