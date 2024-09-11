from marshmallow import Schema, fields, ValidationError

SchemaMessage = Schema.from_dict(
    {"id": fields.Number(), "nome": fields.Str(), "operacao": fields.Str(), "quantidade": fields.Number(), "origem": fields.Str(), "destino": fields.Str()}
)

class ValidatorService:

    def validate(self, message):
        try:
            print("validando")
            # Parse the schema
            resultado = SchemaMessage().load(message)

            print("depois validaçao")
            # Print the validation result
            print(resultado)  # Whether it adheres to the schema
        except ValidationError as error:
            print(error.messages)
            print(error.valid_data)
            raise error
