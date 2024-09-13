import json
import boto3
from marshmallow import ValidationError

from service.processor_delivery import SNSDeliveryService
from service.processor_validation import ValidatorService
from usecase.processor_use_case import EventProcessorUseCase

# Intancia cliente de SNS
sns = boto3.client('sns', region_name='us-east-1')

def handler(event, context):
    """
    Handler do Lambda para recepcionar a mensagem da fila
    Parameters:
    event (object): evento contendo informação da mensagem a ser processada
    context (object): contexto de processameto da lambda
    """

    print("Recebendo mensagem do produtor via fila SQS")
    print(f"Mensagem recebida {event['Records'][0]['body']}")
    body = json.loads(event['Records'][0]['body'])

    try:
        # Instancia serviços de validação e entrega de mensagem em tópico
        validator_service = ValidatorService()
        delivery_service = SNSDeliveryService(sns)

        # Instancia e execuda use case para processamento da mensagem vinda do evento
        use_case = EventProcessorUseCase(validator_service, delivery_service)
        use_case.execute(body)
        return {
            'statusCode': 200,
            'body': 'Function executed successfully!'
        }
    except ValidationError as validationError:
        print(f"Erro de validacao: {validationError}")
        raise validationError
    except Exception as error:
        print(f"Erro interno: {error}")
        raise error