import json

def handler(event, context):
    try:
        print("HELLO")
        print(f"event=${event['Records'][0]['body']}")
        body=json.loads(event['Records'][0]['body'])
        first_name=body['first_name']
        last_name=body['last_name']
        print(f"The first_name is: {first_name}")
        print(f"The last_name is: {last_name}")
        message = 'Hello {} {}!'.format(first_name, last_name)
        return {
            'message' : message
        }
    except Exception as error:
        print("An exception occurred:", error)