"""
Event Processor Use Case module: Lógica de processamento da mensagem recebida.
"""

from service.processor_delivery import SNSDeliveryService
from service.processor_validation import ValidatorService


class EventProcessorUseCase:
    """Classe de use case do event processor"""

    def __init__(self, validator_service: ValidatorService, sns_delivery_service: SNSDeliveryService):
        """
        Inicializa classe de use case passando os serviços de validação de mensagem e envio para tópico
        Parameters:
        validator_service (ValidatorService): Serviço de validação da mensagem.
        sns_delivery_service (SNSDeliveryService): Serviço de publicação de mensagem no tópico para o cliente
           correspondente.
        """

        self.validator_service = validator_service
        self.sns_delivery_service = sns_delivery_service

    def execute(self, message):
        """
        Executa o lógica do event processor.
        Parameters:
        mensage (object): mensagem recebida
        """

        # Valida a mensagem recebida contra um schema
        self.validator_service.validate(message)
        # Publica a mensagem no tópico correspondente
        self.sns_delivery_service.publish_message(message)
