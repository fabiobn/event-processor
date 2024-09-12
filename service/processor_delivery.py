import json
import os

AWS_REGION = os.environ['AWS_REGION']
TOPIC_NAME_CLIENT1=os.environ['TOPIC_NAME_CLIENT1']
TOPIC_NAME_CLIENT2=os.environ['TOPIC_NAME_CLIENT2']
TOPIC_NAME_CLIENT3=os.environ['TOPIC_NAME_CLIENT3']
EVENT_PROCESSOR_QUEUE_DLQ=os.environ['EVENT_PROCESSOR_QUEUE_DLQ']

TOPIC_ARN1=f'arn:aws:sns:{AWS_REGION}:000000000000:{TOPIC_NAME_CLIENT1}'
TOPIC_ARN2=f'arn:aws:sns:{AWS_REGION}:000000000000:{TOPIC_NAME_CLIENT2}'
TOPIC_ARN3=f'arn:aws:sns:{AWS_REGION}:000000000000:{TOPIC_NAME_CLIENT3}'

SQS_QUEUE_DLQ_URL=f'http://sqs.{AWS_REGION}.localhost.localstack.cloud:4566/000000000000/{EVENT_PROCESSOR_QUEUE_DLQ}'

class SNSDeliveryService:

    def __init__(self, sns_client):
        self.sns_client = sns_client

    def publish_message(self, message):
        try:
            print("Sending message to SNS 123")
            print(f"Message to send to SNS 123: {json.dumps(message, indent=2)}")

            topic_to_send = self.__define_destination_topic(message['destino'])
            message_group_id = self.__define_group_id(message['destino'])

            print(f"Topic: {topic_to_send}")
            print(f"Topic: {message['destino']}")
            print(f"Topic: {message['id']}")
            # publish message to sns
            snsResponse = self.sns_client.publish(
                TargetArn=topic_to_send,
                Message=json.dumps(message, indent=2),
                Subject='PROCESSAMENTO DE INFORMACAO',
                MessageGroupId=str(message_group_id),
                MessageDeduplicationId=str(message['id'])
            )
            print(f"Message sent to SNS: {json.dumps(message, indent=2)}")
        except Exception as error:
            print("An exception occurred:", error)
            raise error

    def __define_destination_topic(self, cliente_destino) -> str:
        print(f'__define_destination_topic {cliente_destino}')
        print(f'__define_destination_topic {TOPIC_ARN1}')
        print(f'__define_destination_topic {TOPIC_ARN2}')
        print(f'__define_destination_topic {TOPIC_ARN3}')
        if cliente_destino == "loja A":
           return TOPIC_ARN1
        elif cliente_destino == "loja B":
            return TOPIC_ARN2
        else:
            return TOPIC_ARN3

    def __define_group_id(self, cliente_destino) -> str:
        if cliente_destino == "loja A":
           return "A"
        elif cliente_destino == "loja B":
            return "B"
        else:
            return "C"

class SQSDeliveryService:

    def __init__(self, sqs_client):
        self.sqs_client = sqs_client

    def send_message(self, message):
        try:
            print(f"Sending message to SQS")
            print(f"Message to send to SQS: {json.dumps(message, indent=2)}")
            print(f"SQS: {SQS_QUEUE_DLQ_URL}")

            # publish message to sns
            sqsResponse = self.sqs_client.send_message(
                QueueUrl=SQS_QUEUE_DLQ_URL,
                MessageBody=json.dumps(message, indent=2)
            )
            print(f"Message sent to SQS: {json.dumps(message, indent=2)}")
        except Exception as error:
            print("An exception occurred:", error)
            raise error