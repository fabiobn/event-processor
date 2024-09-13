"""
Event Processor Validation module: Serviço de validação de mensagem.
"""

from marshmallow import Schema, fields, ValidationError

# Definição de schema para validação da mensagem
SchemaMessage = Schema.from_dict(
    {"id": fields.Number(), "nome": fields.Str(), "operacao": fields.Str(), "quantidade": fields.Number(), "origem": fields.Str(), "destino": fields.Str()}
)

class ValidatorService:
    """Classe de serviço para validação de mensagem recebida"""

    def validate(self, message):
        """
        Valida mensagem
        Parameters:
        mensage (object): mensagem recebida
        """

        try:
            print("Validando mensagem")

            SchemaMessage().load(message)

            print("Mensagem validada")
        except ValidationError as error:
            print(f"Mensagem incorreta: {error.messages}")
            raise error
