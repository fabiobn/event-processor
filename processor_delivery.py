import json

TOPIC_ARN1="arn:aws:sns:us-east-1:000000000000:event-processor-client1.fifo"
TOPIC_ARN2="arn:aws:sns:us-east-1:000000000000:event-processor-client2.fifo"
TOPIC_ARN3="arn:aws:sns:us-east-1:000000000000:event-processor-client1.fifo"

def send_message(sns, message):
    try:
        print(f"Sending message to SNS")
        print(f"Message to send to SNS: {json.dumps(message, indent=2)}")
        print(f"Topic: {TOPIC_ARN1}")
        # publish message to sns
        snsResponse = sns.publish(
            TargetArn=TOPIC_ARN1,
            Message=json.dumps(message, indent=2),
            Subject='TESTE',
            MessageGroupId='1',
            MessageDeduplicationId='1'
        )
        print(f"Message sent to SNS: {json.dumps(message, indent=2)}")
    except Exception as error:
        print("An exception occurred:", error)