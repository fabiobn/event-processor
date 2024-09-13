"""
Event Processor Delivery module: Serviço de entrega de mensagem para tópico de cliente correspondente.
"""

import json
import os

# Definição de variáveis com base nas informações de environments
AWS_REGION = os.environ['AWS_REGION']

# Nome do tópico referente a cada cliente
TOPIC_NAME_CLIENT1=os.environ['TOPIC_NAME_CLIENT1']
TOPIC_NAME_CLIENT2=os.environ['TOPIC_NAME_CLIENT2']
TOPIC_NAME_CLIENT3=os.environ['TOPIC_NAME_CLIENT3']

# ARN do tópico referente a cada cliente
TOPIC_ARN1=f'arn:aws:sns:{AWS_REGION}:000000000000:{TOPIC_NAME_CLIENT1}'
TOPIC_ARN2=f'arn:aws:sns:{AWS_REGION}:000000000000:{TOPIC_NAME_CLIENT2}'
TOPIC_ARN3=f'arn:aws:sns:{AWS_REGION}:000000000000:{TOPIC_NAME_CLIENT3}'

class SNSDeliveryService:
    """Classe de serviço para envio de mensagem em tópico destino"""

    def __init__(self, sns_client):
        """
        Inicializa classe de serviço para publicação em tópico SNS
        Parameters:
        sns_client (BaseClient): SNS Client para publicação em tópico
        """
        self.sns_client = sns_client

    def publish_message(self, message):
        """
        Publica mensagem em tópico SNS
        Parameters:
        message (object): mensagem recebida
        """
        try:
            print("Publicando mensagem no SNS")

            # Define tópico, group id e id deduplicação para envio da mensagem
            topic_to_send = self.__define_destination_topic(message['destino'])
            message_group_id = self.__define_group_id(message['destino'])
            message_id = self.__define_group_id(message['id'])
            print(f"Topico definido: {topic_to_send}")
            print(f"Group id definido: {message_group_id}")
            print(f"Id da mensagem: {message_id}")

            self.sns_client.publish(
                TargetArn=topic_to_send,
                Message=json.dumps(message, indent=2),
                Subject='PROCESSAMENTO DE INFORMACAO',
                MessageGroupId=str(message_group_id),
                MessageDeduplicationId=str(message_id)
            )
            print(f"Mensagem enviada para SNS com sucesso: {json.dumps(message, indent=2)}")
        except Exception as error:
            print("Falha no envio da mensagem para SNS: ", error)
            raise error

    def __define_destination_topic(self, cliente_destino) -> str:
        """
        Define tópico de destino, a partir da informação destino da mensagem recebida
        Parameters:
        cliente_destino (str): informação de destino da mensagem recebida
        """
        if cliente_destino == "loja A":
           return TOPIC_ARN1
        elif cliente_destino == "loja B":
            return TOPIC_ARN2
        else:
            return TOPIC_ARN3

    def __define_group_id(self, cliente_destino) -> str:
        """
        Define group id da mensagem a ser enviada para o tópico, a partir da informação destino da mensagem recebida
        Parameters:
        cliente_destino (str): informação de destino da mensagem recebida
        """
        if cliente_destino == "loja A":
           return "A"
        elif cliente_destino == "loja B":
            return "B"
        else:
            return "C"