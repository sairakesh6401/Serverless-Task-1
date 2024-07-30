import json
import boto3 # type: ignore
from botocore.exceptions import ClientError # type: ignore

def sendEmail(event, context):
    body = json.loads(event['body'])
    receiver_email = body.get('receiver_email')
    subject = body.get('subject')
    body_text = body.get('body_text')

    if not receiver_email or not subject or not body_text:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Missing required fields"})
        }

    SENDER = "your_email@example.com"
    AWS_REGION = "us-west-2"
    CHARSET = "UTF-8"

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [receiver_email],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Email sent successfully"})
    }