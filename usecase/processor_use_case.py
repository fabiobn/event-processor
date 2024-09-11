from service.processor_delivery import SNSDeliveryService
from service.processor_validation import ValidatorService


class EventProcessorUseCase:

    def __init__(self, validator_service: ValidatorService, sns_delivery_service: SNSDeliveryService):
        self.validator_service = validator_service
        self.sns_delivery_service = sns_delivery_service

    def execute(self, message):
        self.validator_service.validate(message)
        self.sns_delivery_service.publish_message(message)
