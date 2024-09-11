import json

import boto3

from service.processor_delivery import SNSDeliveryService, SQSDeliveryService
from service.processor_validation import ValidatorService
from usecase.processor_use_case import EventProcessorUseCase

sns = boto3.client('sns', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')
#json_region = os.environ['AWS_REGION']

def handler(event, context):
    print("HELLO")
    print(f"event=${event['Records'][0]['body']}")
    body = json.loads(event['Records'][0]['body'])

    try:
        print("HELLO")
        validator_service = ValidatorService()
        delivery_service = SNSDeliveryService(sns)

        use_case = EventProcessorUseCase(validator_service, delivery_service)
        use_case.execute(body)
    except Exception as validationError:
        print("An validation exception occurred:", validationError)
        sqs_delivery_service = SQSDeliveryService(sqs)
        sqs_delivery_service.send_message(body)
    #except Exception as error:
        #print("An exception occurred:", error)
        #raise error